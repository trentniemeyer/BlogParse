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

class BlogParser (object):

    #url = "http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html"

    def __init__(self, url, forceReindex):
        self.url = url
        self.es = elasticsearch.Elasticsearch()
        #TODO: See if URL already exists and 'forceReIndex' is true
        self.response = urlopen(url)
        self.html = self.response.read().decode('utf-8')
        self.soup = BeautifulSoup.BeautifulSoup(self.html)
        self.data = {}

    def parseMainContent (self):
        postBody = self.soup.find(id="post")
        #TODO-LOW: If PostBody Not Found, Throw Error.  Write failing test for this, it means the site changed
        postBodyText = ''
        #TODO-MID: Find Images
        for t in postBody.contents:
            if type(t) is BeautifulSoup.NavigableString:
                postBodyText += t
        self.data['text']= postBodyText,
        self.data['length'] = len(postBodyText)

    def parseLocation(self):
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

    def saveBlogAndAuthor (self):
        result = self.es.index(index='blogs', doc_type='blog', body=json.dumps (self.data))
        print result
        #TODO-NOW Save Author

    def parseAuthor (self):
        authorHref = self.soup.find("a", attrs={'class' : 'avatar'})['href']
        authorLink = "http://www.travelpod.com" + authorHref

