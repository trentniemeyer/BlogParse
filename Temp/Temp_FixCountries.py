import ElasticMappings
import TravelPodParser
import Util
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

client = Elasticsearch([Util.config['eshost']])

def fixlocationparsing ():
    response = ElasticMappings.Blog.search()[0:500].execute()

    logger.info("Reparsing location info for %d Hits:" % len(response.hits))

    for blog in response:
        parser = TravelPodParser.TravelPodBlogParser(blog.url)
        parser.parselocation()

        if (parser.isafrica):
            blog.city = parser.blog.city
            blog.state = parser.blog.state
            blog.country = parser.blog.country
            blog.save()
        else:
            logger.info("Deleting blog: " + blog.meta.id)
            blog.delete ()

def fixcongo():
    s = ElasticMappings.Blog.search ()[0:200]
    response = s.query('match', country='Congo - The Dem. Repub.').execute()

    print len(response.hits)
    for blog in response:
        blog.country = 'Congo'
        blog.save()

def lowercasecountries ():
    response = ElasticMappings.Blog.search()[0:10000].execute()
    processed = 0
    for blog in response.hits:
        try:
            if hasattr(blog, "city"):
                blog.city = blog.city.lower ()
            else:
                blog.city = ""
            if hasattr(blog, "state"):
                blog.state = blog.state.lower()
            else:
                blog.state = ""
            if hasattr(blog, "country"):
                blog.country = blog.country.lower()
            else:
                blog.country = ""
            blog.save()
            processed+=1
            if processed%100 == 0:
                print processed
        except:
            print(blog._id)

lowercasecountries ()