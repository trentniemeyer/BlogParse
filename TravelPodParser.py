import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String, Date, Integer, Search, Nested
from datetime import datetime
import json
import BeautifulSoup
import Util

class Parser (object):

    def __init__(self, url, forceReindex):
        self.url = url
        self.client = Elasticsearch()
        self.itemexists = False

        self.itemid = self.getitemid()
        if (self.itemid == False):
            self.html = Util.geturldata(url)
        else:
            self.html = Util.getobjectfromazure(self.itemid)
            self.itemexists = True

        self.soup = BeautifulSoup.BeautifulSoup(self.html)

    def getitemid (self):
        raise NotImplementedError("you must define the item lookup for this class")

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

class BlogParser (Parser):

    def __init__(self, url, forceReindex):
        Blog.init()
        Parser.__init__(self, url, forceReindex)
        self.blog = Blog()
        self.blog.url = url

    def getitemid(self):
        response = self.client.search(
            index="blogs",
            body={
                "query":{
                    "match": {
                      "url.rawurl": self.url
                    }
                  }
            }
        )

        if (len (response['hits']['hits']) > 0):
            return response['hits']['hits'][0]['_id']
        else:
            return False

    def parseall (self):
        self.parsemaincontent()
        self.parselocation()
        self.getauthorurl()
        self.parsetrip()

    def parsemaincontent (self):
        postBody = self.soup.find(id="post")

        postBodyText = ''
        #TODO-MID: Find Images
        for t in postBody.contents:
            if type(t) is BeautifulSoup.NavigableString:
                postBodyText += t

        self.blog.body = postBodyText
        self.blog.title = self.soup.find("meta", {"name": "twitter:name"})['content']

    def parselocation(self):
        locationStack = []
        titleContents = self.soup.find("p", attrs={'class' : 'meta'}).contents
        for t in titleContents:
            if type(t) is BeautifulSoup.Tag:
                if t.name == 'a':
                    locationStack.append(t.string)
                elif t.name == 'span':
                    self.blog.postdate = datetime.strptime(t.string, '%A, %B %d, %Y')

        self.blog.city = locationStack[0]
        self.blog.state = locationStack[1]
        self.blog.country = locationStack[2]

    def getauthorurl (self):
        authorHref = self.soup.find("a", attrs={'class' : 'avatar'})['href']
        authorLink = "http://www.travelpod.com" + authorHref
        return authorLink

    def parsetrip (self):
        self.blog.trip = 'http://www.travelpod.com' + self.soup.find("a", attrs={'title' : 'See more entries in this travel blog'})['href']

    def save (self):
        if (self.itemexists == False):
            blogid = Util.generatebase64uuid()
            Util.putobjectinazure(blogid, self.url, self.html)
            self.blog.meta.id = blogid
        else:
            self.blog.meta.id = self.itemid

        self.blog.save()

class AuthorParser (Parser):

    def __init__(self, url, forceReindex):
        Author.init()
        Parser.__init__(self, url, forceReindex)
        self.author = Author()
        self.author.url = url

    def getitemid(self):
        response = self.client.search(
            index="authors",
            body={
                "query":{
                    "match": {
                      "url.rawurl": self.url
                    }
                  }
            }
        )

        if (len (response['hits']['hits']) > 0):
            return response['hits']['hits'][0]['_id']
        else:
            return False

    def parselogsummary (self):
        self.author.username = self.soup.find("meta", {"property":"og:title"})['content']
        summary = self.soup.find("div", attrs={'class' : 'bubble'}).contents
        for t in summary:
            if type(t) is BeautifulSoup.Tag:
                if t.name == 'span':
                    self.author.blogcount = str(t.string).split(' ')[0]
        self.author.photo = self.soup.find(id="profile_pic")['src']

    def parsetrips (self):
        print ("TODO")

    def save (self):
        if (self.itemexists == False):
            if (hasattr(self.author.meta, 'id') == False):
                authorid = Util.generatebase64uuid()
                self.author.meta.id = authorid
            Util.putobjectinazure(self.author.meta.id, self.url, self.html)
        else:
            self.author.meta.id = self.itemid

        self.author.save()

class AuthorTripParser (Parser):
    def getitemid(self):
        return False

    def __init__(self, url, forcereindex = False):
        Parser.__init__(self, url, forcereindex)

    def parsebloglinks (self):
        self.bloglist = []
        for div in self.soup.findAll("div", {"class":"blog_data"}):
            self.bloglist.append(div.contents[1]['href'])
        return self.bloglist






