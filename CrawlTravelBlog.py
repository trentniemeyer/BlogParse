import logging
import LoggerConfig
import ElasticMappings
from TravelBlogParser import TravelBlogBlogParser, TravelPodAuthorParser,TravelBlogAuthorTripParser, TravelBlogMainSectionParser
import Util



def init ():
    ElasticMappings.Blog.init()
    ElasticMappings.Author.init()

def shouldcontinue (url, blogsparsedcount):
    return url <> False and blogsparsedcount <= 100

class Crawler (object):#TODO: Refactor

    BASE_URL = "https://www.travelblog.org/Africa/"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mainurl = self.BASE_URL + "blogs-page-1.html"
        self.currentblogparser = None
        self.authorparser = None
        self.blogsparsed = 0

    def process(self):

        while self.__shouldcontinueparsingmain():

            sectionparser = TravelBlogMainSectionParser(self.mainurl)
            sectionparser.loaditem()

            for blogurl in sectionparser.parsebloglinks(addonlyenglish=True):

                if self.__processblog (blogurl, True):

                    if (self.currentblogparser.blog.trip):
                        tripparser = TravelBlogAuthorTripParser (self.currentblogparser.blog.trip)
                        tripparser.loaditem()

                        tripurls = tripparser.parsebloglinks()
                        self.logger.info("Parsing {0} trip blogs for author: {1}".format(len(tripurls),self.authorparser.author.username))

                        for authorblogurl in tripurls:
                            self.__processblog(authorblogurl)
                    else:
                        currentauthorbloglisturl = self.authorparser.url

                        while (currentauthorbloglisturl <> False):
                            authorblogparser = TravelBlogMainSectionParser(currentauthorbloglisturl)
                            authorblogparser.loaditem()

                            allauthorsurls = authorblogparser.parsebloglinks()
                            self.logger.info("No Trip Found, Parsing {0} ALL blogs for author: {1}".format(len(allauthorsurls),self.authorparser.author.username))
                            for authorblog in allauthorsurls:
                                self.__processblog(authorblog)

                            currentauthorbloglisturl = authorblogparser.getnext(self.authorparser.url)

                    self.authorparser.save()

            self.mainurl = sectionparser.getnext(self.BASE_URL)


    def __shouldcontinueparsingmain (self):
        return self.blogsparsed <= 100 and self.mainurl <> False

    def __processblog (self, blogurl, resetauthor = False):

        self.currentblogparser = TravelBlogBlogParser(blogurl)

        if self.currentblogparser.loaditem(False):
            self.currentblogparser.parseall()

            if resetauthor:
                self.authorparser = TravelPodAuthorParser(self.currentblogparser.getauthorurl())
                self.authorparser.loaditem()
                self.authorparser.parselogsummary()

            if self.currentblogparser.isvalidforindex():
                self.currentblogparser.blog.setauthor(self.authorparser.author)
                self.currentblogparser.save()
                self.blogsparsed+=1

            self.authorparser.author.add_blog(self.currentblogparser.blog)
            return True
        else:
            return False


if __name__ == '__main__':

    crawler = Crawler()

    crawler.process()

