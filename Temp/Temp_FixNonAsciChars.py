import urllib2
import BeautifulSoup

import ElasticMappings
import LoggerConfig
import Util
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

def test ():
    page = urllib2.urlopen('http://www.travelpod.com/travel-blog-entries/modernoddyseus/19/1408458921/tpod.html')

    rawdata = page.read()

    encoding = page.info().getparam("charset")

    html = rawdata.decode (encoding)

    soup = BeautifulSoup.BeautifulSoup(html, convertEntities="html")

    postBody = soup.find(id="post")

    postBodyText = ''

    for t in postBody.contents:
        if type(t) is BeautifulSoup.NavigableString:
            postBodyText += t

    print postBodyText

def fixallblogs ():

    for i in range (0, 3500, 50):

        response = ElasticMappings.Blog.search()[i:i+50].execute()

        logger.info("Processing blogs {0}-{1}".format(i, i+50))

        for blog in response.hits:
            try:
                blog.body = BeautifulSoup.BeautifulSoup(blog.body, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES).text
                blog.save()
            except Exception:
                logger.exception("Couldn't parse blog id: {0}".format(blog.meta.id))


fixallblogs ()