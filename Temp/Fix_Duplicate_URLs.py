import ElasticMappings
import LoggerConfig
import Util
import logging
import TravelPodParser
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

#before 3462, expected 3442 when done
client = Elasticsearch([Util.config['eshost']])
#blog = "http://www.travelpod.com/travel-blog-entries/acres_wild/6/1435194427/tpod.html"
response = client.search(
            index="blogs",
            body={
                "aggs" : {
                    "duplicate_urls" : {
                        "terms" : {
                            "field" : "url.rawurl",
                            "size": 500,
                            "min_doc_count":2
                        }
                    }
                }
            }
        )




for urlcount in response['aggregations']['duplicate_urls']['buckets']:
    blog = urlcount['key']
    duplicateblogresponse = client.search (index="blogs",
    body={
        "size": 1,
        "query": {
            "match": {
              "url.rawurl": blog
            }
        },
        "fields":"_id"
    })
    idtodelete = duplicateblogresponse['hits']['hits'][0]['_id']
    client.delete(index="blogs", doc_type="blog",id=idtodelete)

