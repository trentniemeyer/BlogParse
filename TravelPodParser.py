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

url = "http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html"
es = elasticsearch.Elasticsearch()
#TODO: See if URL already exists and 'forceReIndex' is true
response = urlopen(url)
html = response.read().decode('utf-8')
soup = BeautifulSoup.BeautifulSoup(html)
data = {}

def parseMainContent ():
    postBody = soup.find(id="post")
    #TODO-LOW: If PostBody Not Found, Throw Error.  Write failing test for this, it means the site changed
    postBodyText = ''
    #TODO-MID: Find Images
    for t in postBody.contents:
        if type(t) is BeautifulSoup.NavigableString:
            postBodyText += t
    data['text']= postBodyText,
    data['length'] = len(postBodyText)

def parseLocation():
    locationStack = []
    date = ''
    titleContents = soup.find("p", attrs={'class' : 'meta'}).contents
    #TODO-LOW: If titleContents Not Found, Throw Error.  Write failing test for this, it means the site changed
    #TODO-MID: Find Images
    for t in titleContents:
        if type(t) is BeautifulSoup.Tag:
            if t.name == 'a':
                locationStack.append(t.string)
            elif t.name == 'span':
                date = DateTime(t.string)

    data['city'] = locationStack[0]
    data['state'] = locationStack[1]
    data ['country'] = locationStack[2]
    data['postDate'] = date.strftime('%Y-%m-%dT%H:%M:%S%z')

def parseAuthor ():
    print 'do this'

def parseTrip ():
    print 'do this too'

def saveBlogAndAuthor ():
    result = es.index(index='blogs', doc_type='blog', body=json.dumps (data))
    print result
    #TODO-NOW Save Author

if __name__ == '__main__':
    parseMainContent()
    parseLocation()
    parseAuthor()
    parseTrip ()
    saveBlogAndAuthor()


