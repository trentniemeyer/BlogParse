from elasticsearch import Elasticsearch
from datetime import datetime
import BeautifulSoup
import Util
import ElasticMappings
import re
import logging

class Parser (object):

    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.client = Elasticsearch([Util.config['eshost']])
        self.itemexists = False
        self.oktoparse = True
        self.itemid = self.getitemid()

    def getitemid (self):
        raise NotImplementedError("you must define the item lookup for this class")

    def loaditem (self, forcereindex = True, cookiedict = None):
        if (self.itemid == False):
            self.html = Util.geturldata(self.url, cookiedict)
            self.logger.info("Parsing: {0}".format(self.url))
        elif (forcereindex):
            self.html = Util.gettextobjectfromazure(self.itemid)
            self.itemexists = True
            self.logger.info("RE-Parsing from Azure".format(self.url))
        else:
            self.oktoparse = False

        if (self.oktoparse):
            self.soup = BeautifulSoup.BeautifulSoup(self.html, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
        else:
            self.logger.info("skipping reindex for '{0}'".format(self.url))

        return self.oktoparse


class BlogParser (Parser):

    def loaditem(self, forcereindex = True, cookiedict = None):
        self.blog = ElasticMappings.Blog()
        self.blog.url = self.url
        return Parser.loaditem(self, forcereindex, cookiedict)

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

        for t in postBody.contents:
            if type(t) is BeautifulSoup.NavigableString:
                postBodyText += t

        firstthumbnailimagediv = self.soup.find('div',  attrs={'class':re.compile('^inline-thumb')})

        if (firstthumbnailimagediv):
            thumbnailimage = firstthumbnailimagediv.findNext('img')['src']
            thumbnailimage = thumbnailimage.replace ("xlarge", "large")
            self.blog.thumbnailimage = thumbnailimage

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

        self.blog.city = ''
        self.blog.state = ''
        self.blog.country = ''
        if (len(locationStack) == 3):
            self.blog.country = locationStack[2]
            self.blog.state = locationStack[1]
            self.blog.city = locationStack[0]
        elif (len(locationStack) == 2):
            self.blog.country = locationStack[1]
            self.blog.state = locationStack[0]
        else:
            raise NotImplementedError("Single location field not handled yet")

        self.isafrica = Util.isafrica(self.blog.country)

    def parseimage (self):
        self.soup.find()

    def getauthorurl (self):
        authorHref = self.soup.find("div", attrs={'class':'profile'}).findNext ('a')['href']
        authorLink = "http://www.travelpod.com" + authorHref
        return authorLink

    def parsetrip (self):
        self.blog.trip = 'http://www.travelpod.com' + self.soup.find("a", attrs={'title' : 'See more entries in this travel blog'})['href']

    def save (self):
        if (self.itemexists == False):
            blogid = Util.generatebase64uuid()
            Util.puttextobjectinazure(blogid, self.url, self.html)
            self.blog.meta.id = blogid

            if (hasattr(self.blog, 'thumbnailimage') and self.blog.thumbnailimage):
                Util.copywebimageandputinazure(self.blog.meta.id, self.blog.thumbnailimage)
        else:
            self.blog.meta.id = self.itemid

        self.blog.save()

class AuthorParser (Parser):

    def loaditem(self, forcereindex = True, cookiedict = None):
        self.author = ElasticMappings.Author()
        self.author.url = self.url
        didload = Parser.loaditem(self, forcereindex, cookiedict)
        if(self.itemexists):
            self.author.get(id=self.itemid)
        return didload

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
                    blogcount = str(t.string).split(' ')[0]
                    self.author.blogcount = blogcount.translate(None, ",")
        self.author.photo = self.soup.find(id="profile_pic")['src']

    def parsetrips (self):
        print ("TODO")

    def save (self):
        if (self.itemexists == False):
            if (hasattr(self.author.meta, 'id') == False):
                authorid = Util.generatebase64uuid()
                self.author.meta.id = authorid
            Util.puttextobjectinazure(self.author.meta.id, self.url, self.html)
        else:
            self.author.meta.id = self.itemid

        self.author.save()

class AuthorTripParser (Parser):
    def getitemid(self):
        return False

    def parsebloglinks (self):
        self.bloglist = []
        for div in self.soup.findAll("div", {"class":"blog_data"}):
            self.bloglist.append(div.contents[1]['href'])
        return self.bloglist

class MainSectionParser (Parser):
    def getitemid(self):
        return False

    def loaditem(self, forcereindex = True, cookiedict = None):
        cookiedict = {'tweb_order':'time'} #sort by time so we can parse latest first (instead of most popular)
        Parser.loaditem(self,forcereindex, cookiedict)

    def parsebloglinks (self):
        self.bloglist = []
        for div in self.soup.findAll('div',  attrs={'class':re.compile('^blog_info$')}):
            if (Util.istextenglish(div.findAll('p')[1].text)):
                self.bloglist.append(div.findNext ('a')['href']);
        return self.bloglist

