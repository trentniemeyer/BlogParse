from elasticsearch_dsl import DocType, String, Date, Integer, Nested
import Util

class Blog(DocType):
    city = String(index='not_analyzed')
    state = String(index='not_analyzed')
    country = String(index='not_analyzed')
    title = String(analyzer='snowball', fields={'rawtitle': String(index='not_analyzed')})
    url = String(analyzer='snowball', fields={'rawurl': String(index='not_analyzed')})
    body = String(analyzer='snowball')
    trip = String(index='not_analyzed')
    postdate = Date()
    length = Integer()

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

    class Meta:
        index = 'authors'

    def add_blog (self, blog):
        self.blogs.append (
            {'id': blog.meta.id, 'url': blog.url, 'length:': blog.length, 'trip': blog.trip, 'title': blog.title,
             'country':blog.country, 'state': blog.state, 'city': blog.city, 'postdate': blog.postdate
            }
        )
