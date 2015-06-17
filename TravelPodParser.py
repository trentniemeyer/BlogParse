from elasticsearch import Elasticsearch
from datetime import datetime
import BeautifulSoup
import Util
import ElasticMappings

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

class BlogParser (Parser):

    def __init__(self, url, forceReindex):
        ElasticMappings.Blog.init()
        Parser.__init__(self, url, forceReindex)
        self.blog = ElasticMappings.Blog()
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
        ElasticMappings.Author.init()
        Parser.__init__(self, url, forceReindex)
        self.author = ElasticMappings.Author()
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






