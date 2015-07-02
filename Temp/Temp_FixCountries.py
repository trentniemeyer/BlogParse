import ElasticMappings
import TravelPodParser
import Util
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

client = Elasticsearch([Util.config['eshost']])

response = ElasticMappings.Blog.search()[0:500].execute()

logger.info("Reparsing location info for %d Hits:" % len(response.hits))

for blog in response:
    parser = TravelPodParser.BlogParser(blog.url)
    parser.parselocation()
    blog.city = parser.blog.city
    blog.state = parser.blog.state
    blog.country = parser.blog.country
    blog.save()

