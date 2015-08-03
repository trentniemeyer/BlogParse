import Util
import ElasticMappings
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

client = Elasticsearch([Util.config['eshost']])

def fixsmallblogs ():
    client = Elasticsearch([Util.config['eshost']])

    response = client.search(
                index="blogs",
                body={
                    "size": 400,
                      "query" : {
                        "range": {
                          "length": {
                            "lte": 50
                          }
                        }
                      }
                }
            )

    for hit in response['hits']['hits']:
        print hit['_id']
        client.delete('blogs','blog', hit['_id'])

def removealltravelblogblogs ():
    client = Elasticsearch([Util.config['eshost']])

    response = client.search(
                index="blogs",
                body={
                    "size": 400,
                     "query": {
                        "prefix": {
                          "url.rawurl": {
                            "value": "http://www.travelblog.org"
                          }
                        }
                      }
                }
            )



    for hit in response['hits']['hits']:
        print hit['_id']
        Util.deletefromazure(hit['_id'])
        client.delete('blogs','blog', hit['_id'])

removealltravelblogblogs()