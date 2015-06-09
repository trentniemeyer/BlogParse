import elasticsearch
from DateTime import DateTime

import BeautifulSoup
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

url = "http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html"
response = urlopen(url)
html = response.read().decode('utf-8')
soup = BeautifulSoup.BeautifulSoup(html)
postBody = soup.find(id="post")
postBodyText = ''
for t in postBody.contents:
    if type(t) is BeautifulSoup.NavigableString:
        postBodyText += t
print postBodyText
print '-------'

locationStack = []
date = ''
titleContents = soup.find("p", attrs={'class' : 'meta'}).contents
for t in titleContents:
    if type(t) is BeautifulSoup.Tag:
        if t.name == 'a':
            locationStack.append(t.string)
        elif t.name == 'span':
            date = DateTime(t.string)
            #date = time.strptime(t.string, '%A, %B %d, %Y')
print locationStack
print date

es = elasticsearch.Elasticsearch()
es.index(index='blogs', doc_type='blog', body={
    'url':url,
    'postDate': date.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'city':locationStack[0],
    'state':locationStack[1],
    'country':locationStack[2],
    'text': postBodyText,
    'length': len(postBodyText)
})


