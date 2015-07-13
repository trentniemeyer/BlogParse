import ElasticMappings
import TravelPodParser
import Util
import LoggerConfig
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

response = ElasticMappings.Blog.search()[0:3500].execute()

count = 0
for blog in response:
    if Util.istextenglish(blog.body) == False:
        blog.delete()
        count+=1

logger.info("Deleted {0} foreign blogs".format(count))
