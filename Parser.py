import logging
import BeautifulSoup
from elasticsearch import Elasticsearch
import Util
import ElasticMappings
import abc


class Parser (object):

    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.client = Elasticsearch([Util.config['eshost']])
        self.oktoparse = True
        self.itemid = self.getitemid()

    @abc.abstractmethod
    def getitemid (self):
        return False

    def itemexists (self):
        return self.itemid != False

    def loaditem (self, forcereindex = True, cookiedict = None):
        if (self.itemid == False):
            self.html = Util.geturldata(self.url, cookiedict)
            self.logger.info("Parsing: {0}".format(self.url))
        elif (forcereindex):
            self.html = Util.gettextobjectfromazure(self.itemid)
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
        self.isafrica = False
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

    @abc.abstractmethod
    def parsemaincontent (self):
        return

    @abc.abstractmethod
    def parselocation (self):
        return

    @abc.abstractmethod
    def getauthorurl (self):
        return

    @abc.abstractmethod
    def parsetrip (self):
        return

    def parseall (self):
        self.parsemaincontent()
        self.parselocation()
        self.getauthorurl()
        self.parsetrip()

    def isvalidforindex(self):
        return self.isafrica and Util.istextenglish(self.blog.body) and len(self.blog.body) > 50

    def save (self):
        if (self.itemexists() == False):
            blogid = Util.generatebase64uuid()
            Util.puttextobjectinazure(blogid, self.url, self.html)
            self.blog.meta.id = blogid

            if (hasattr(self.blog, 'thumbnailimage') and self.blog.thumbnailimage):
                Util.resizeimageandputinazure(self.blog.meta.id, self.blog.thumbnailimage)
        else:
            self.blog.meta.id = self.itemid

        self.blog.save()
        return self.blog.meta.id


class AuthorParser (Parser):

    def loaditem(self, forcereindex = True, cookiedict = None):
        self.author = ElasticMappings.Author()
        self.author.url = self.url
        didload = Parser.loaditem(self, forcereindex, cookiedict)
        if(self.itemexists()):
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

    @abc.abstractmethod
    def parselogsummary (self):
        return

    def save (self):
        if (self.itemexists() == False):
            if (hasattr(self.author.meta, 'id') == False):
                authorid = Util.generatebase64uuid()
                self.author.meta.id = authorid
            Util.puttextobjectinazure(self.author.meta.id, self.url, self.html)
        else:
            self.author.meta.id = self.itemid

        self.author.save()
        return self.author.meta.id