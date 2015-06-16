import elasticsearch
from elasticsearch_dsl import DocType, String, Date, Integer, Search, Nested
from datetime import datetime
import json
import BeautifulSoup
import Util

class Parser (object):

    def __init__(self, url, forceReindex):
        self.url = url
        self.es = elasticsearch.Elasticsearch()
        #TODO: See if URL already exists and 'for`ceReIndex' is true

        itemid = self.getitemid()

        if (itemid == False):
            self.html = Util.geturldata(url)
        else:
            self.html = Util.getobjectins3(itemid)

        self.soup = BeautifulSoup.BeautifulSoup(self.html)
        self.data = {}
        self.data['url'] = url

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
        index = 'testblogs'

    def save(self, ** kwargs):
        self.length = len(self.body)
        blogid = Util.generatebase64uuid()
        Util.putobjectins3(blogid, kwargs['html'])
        self.meta.id = blogid
        return super(Blog, self).save()

    def setauthor (self, author):
        #this will throw an error if the id doesn't exist
        if 'id' not in author:
            raise AttributeError ("Author needs an id")
        self.author = {
            'id' : author['id'],
            'url' : author['url'],
            'username' : author['username'],
            'photo' : author['photo'],
            'blogcount' : author['blogcount']
        }


#TODO-HIGH Clean up old way of storing data
class BlogParser (Parser):

    def __init__(self, url, forceReindex):
        Blog.init()
        Parser.__init__(self, url, forceReindex)
        self.blog = Blog()
        self.blog.url = url

    def getitemid(self):
        #TODO-HIGH: Query and get id
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
        date = ''
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

class AuthorParser (Parser):

    def __init__(self, url, forceReindex):
        Parser.__init__(self, url, forceReindex)

    def getitemid(self):
        return False

    def parselogsummary (self):
        self.data['username'] = self.soup.find("meta", {"property":"og:title"})['content']
        summary = self.soup.find("div", attrs={'class' : 'bubble'}).contents
        for t in summary:
            if type(t) is BeautifulSoup.Tag:
                if t.name == 'span':
                    self.data['blogcount'] = str(t.string).split(' ')[0]
        self.data['photo'] = self.soup.find(id="profile_pic")['src']

    def parsetrips (self):
        print ("TODO")

    def save (self, blogs = None):
        id = Util.generatebase64uuid()
        if ('id' in self.data):
            id = self.data['id']
            del self.data['id']

        if (blogs is not None):
            for blog in blogs:
                del blog['text']
                del blog['author']

        self.data['blogs'] = blogs

        result = self.es.index(id = id, index='authors', doc_type='author', body=json.dumps (self.data))
        return result

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






