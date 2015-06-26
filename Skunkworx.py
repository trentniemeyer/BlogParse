from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, String, Date, Integer, Search, Nested
import TravelPodParser
import Util

#Util.deletefromazure("images")

# currentblogparser = TravelPodParser.BlogParser("http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html")
# currentblogparser.parsemaincontent()
# Util.copywebimageandputinazure(currentblogparser.itemid, currentblogparser.blog.thumbnailimage)

# currentblogparser.parseall()
#
# authorLink = currentblogparser.getauthorurl()
# authorparser = TravelPodParser.AuthorParser (authorLink)
# authorparser.parselogsummary()
#
# currentblogparser.blog.setauthor(authorparser.author)
# currentblogparser.save()
#
# authorparser.author.add_blog(currentblogparser.blog)
# authorparser.save()