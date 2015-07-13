from elasticsearch_dsl import DocType, String, Date, Integer, Nested
import Util
from datetime import datetime

class Blog(DocType):
    city = String(index='not_analyzed', store='true')
    state = String(index='not_analyzed', store='true')
    country = String(index='not_analyzed', store='true')
    title = String(analyzer='snowball', store='true', fields={'rawtitle': String(index='not_analyzed')})
    url = String(analyzer='snowball', fields={'rawurl': String(index='not_analyzed')})
    body = String(analyzer='snowball', store='true')
    trip = String(index='not_analyzed')
    thumbnailimage = String(index='not_analyzed')
    postdate = Date()
    length = Integer()
    lastupdated = Date ()

    author = Nested(
        properties={
        'url':  String(analyzer='snowball', fields={'rawurl': String(index='not_analyzed')}),
        'username': String(index='not_analyzed'),
        'photo': String(index='not_analyzed'),
        'id': String(index='not_analyzed'),
        'blogcount': Integer()
        }
    )

    class Meta:
        index = 'blogs'

    def save(self, ** kwargs):
        self.length = len(self.body)
        self.lastupdated = datetime.now()
        return super(Blog, self).save(** kwargs)

    def setauthor (self, author):

        if (hasattr(author.meta, 'id') == False):
            authorid = Util.generatebase64uuid()
            author.meta.id = authorid

        self.author = {
            'id' : author.meta.id,
            'url' : author.url,
            'username' : author.username,
            'photo' : author.photo,
            'blogcount' : author.blogcount
        }

class Author (DocType):
    username = String (index="not_analyzed")
    photo = String (index="not_analyzed")
    blogcount = Integer()
    url = String(analyzer='snowball', fields={'rawurl': String(index='not_analyzed')})
    blogurls = String(index='not_analyzed')
    lastupdated = Date ()

    blogs = Nested(
        properties={
            'id': String(index='not_analyzed'),
            'url': String(analyzer='snowball', fields={'rawurl': String(index='not_analyzed')}),
            'length' : Integer(),
            'trip' : String(analyzer='snowball', fields={'rawurl': String(index='not_analyzed')}),
            'title': String(analyzer='snowball', fields={'rawtitle': String(index='not_analyzed')}),
            'city' : String(index='not_analyzed'),
            'state' : String(index='not_analyzed'),
            'country' : String(index='not_analyzed'),
            'postdate' : Date()
        }
    )


    def save(self, ** kwargs):
        self.lastupdated = datetime.now()
        return super(Author, self).save(** kwargs)

    class Meta:
        index = 'authors'

    def add_blog (self, blog):

        blogid = ''
        if (blog.meta and blog.meta.id):
            blogid = blog.meta.id

        self.blogs.append (
            {'id': blogid, 'url': blog.url, 'length:': len(blog.body), 'trip': blog.trip, 'title': blog.title,
             'country':blog.country, 'state': blog.state, 'city': blog.city, 'postdate': blog.postdate
            }
        )
