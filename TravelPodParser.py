import elasticsearch
from DateTime import DateTime
import json
import BeautifulSoup
import Util

class Parser (object):

    def __init__(self, url, forceReindex):
        self.url = url
        self.es = elasticsearch.Elasticsearch()
        #TODO: See if URL already exists and 'for`ceReIndex' is true
        self.html = Util.geturldata(url)
        self.soup = BeautifulSoup.BeautifulSoup(self.html)
        self.data = {}
        self.data['url'] = url

class BlogParser (Parser):

    def __init__(self, url, forceReindex):
        print url
        Parser.__init__(self, url, forceReindex)

    def parseall (self):
        self.parsemaincontent()
        self.parselocation()
        self.getauthorurl()
        self.parsetrip()

    def parsemaincontent (self):
        postBody = self.soup.find(id="post")
        #TODO-LOW: If PostBody Not Found, Throw Error.  Write failing test for this, it means the site changed
        postBodyText = ''
        #TODO-MID: Find Images
        for t in postBody.contents:
            if type(t) is BeautifulSoup.NavigableString:
                postBodyText += t
        self.data['text']= postBodyText,
        self.data['length'] = len(postBodyText)
        self.data['title'] = self.soup.find("meta", {"name": "twitter:name"})['content']

    def parselocation(self):
        locationStack = []
        date = ''
        titleContents = self.soup.find("p", attrs={'class' : 'meta'}).contents
        #TODO-LOW: If titleContents Not Found, Throw Error.  Write failing test for this, it means the site changed
        #TODO-MID: Find Images
        for t in titleContents:
            if type(t) is BeautifulSoup.Tag:
                if t.name == 'a':
                    locationStack.append(t.string)
                elif t.name == 'span':
                    date = DateTime(t.string)

        self.data['city'] = locationStack[0]
        self.data['state'] = locationStack[1]
        self.data ['country'] = locationStack[2]
        self.data['postDate'] = date.strftime('%Y-%m-%dT%H:%M:%S%z')

    def getauthorurl (self):
        authorHref = self.soup.find("a", attrs={'class' : 'avatar'})['href']
        authorLink = "http://www.travelpod.com" + authorHref
        return authorLink
        #self.authorparser = AuthorParser (authorLink, False)
        #self.authorparser.parselogsummary()

    def parsetrip (self):
        self.data['trip'] = 'http://www.travelpod.com' + self.soup.find("a", attrs={'title' : 'See more entries in this travel blog'})['href']

    def save (self, author = None):

        if author:
            #this will throw an error if the id doesn't exist
            if 'id' not in author:
                raise AttributeError ("Author needs an id")
            self.data['author'] = author

        result = self.es.index(index='blogs', doc_type='blog', body=json.dumps (self.data))
        return result

class AuthorParser (Parser):

    def __init__(self, url, forceReindex):
        Parser.__init__(self, url, forceReindex)

    def parselogsummary (self):
        self.data['username'] = self.soup.find("meta", {"property":"og:title"})['content']
        summary = self.soup.find("div", attrs={'class' : 'bubble'}).contents
        for t in summary:
            if type(t) is BeautifulSoup.Tag:
                if t.name == 'span':
                    self.data['blogCount'] = str(t.string).split(' ')[0]
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

    def __init__(self, url, forcereindex = False):
        Parser.__init__(self, url, forcereindex)

    def parsebloglinks (self):
        self.bloglist = []
        for div in self.soup.findAll("div", {"class":"blog_data"}):
            self.bloglist.append(div.contents[1]['href'])
        return self.bloglist






