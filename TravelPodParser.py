import elasticsearch
from DateTime import DateTime
import json
import BeautifulSoup
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

class Parser (object):

    def __init__(self, url, forceReindex):
        self.url = url
        self.es = elasticsearch.Elasticsearch()
        #TODO: See if URL already exists and 'for`ceReIndex' is true
        self.response = urlopen(url)
        self.html = self.response.read().decode('utf-8')
        self.soup = BeautifulSoup.BeautifulSoup(self.html)
        self.data = {}
        self.data['url'] = url

class BlogParser (Parser):

    def __init__(self, url, forceReindex):
        Parser.__init__(self, url, forceReindex)

    def parseall (self):
        self.parsemaincontent()
        self.parselocation()
        self.parseauthor()
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

    def save (self):
        result = self.es.index(index='blogs', doc_type='blog', body=json.dumps (self.data))
        return result

    def parseauthor (self):
        authorHref = self.soup.find("a", attrs={'class' : 'avatar'})['href']
        authorLink = "http://www.travelpod.com" + authorHref
        self.authorparser = AuthorParser (authorLink, False)
        self.authorparser.parselogsummary()

    def parsetrip (self):
        self.data['trip'] = 'http://www.travelpod.com' + self.soup.find("a", attrs={'title' : 'See more entries in this travel blog'})['href']

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

    def save (self):
        result = self.es.index(index='authors', doc_type='author', body=json.dumps (self.data))
        return result







