import logging

import ElasticMappings
from TravelBlogParser import TravelBlogBlogParser, TravelPodAuthorParser
import Util


def init ():
    ElasticMappings.Blog.init()
    ElasticMappings.Author.init()

def shouldsaveblog(currentblogparser):
    return currentblogparser.isafrica and Util.istextenglish(currentblogparser.blog.body) and len(currentblogparser.blog.body > 50)


if __name__ == '__main__':

    logger = logging.getLogger(__name__)

    blog = "https://www.travelblog.org/Africa/Mozambique/Southern/Inhambane/blog-892855.html"
    currentblogparser = TravelBlogBlogParser(blog)
    currentblogparser.loaditem()
    currentblogparser.parseall()

    authorparser = TravelPodAuthorParser(currentblogparser.getauthorurl())

    authorparser.loaditem()
    authorparser.parselogsummary()

