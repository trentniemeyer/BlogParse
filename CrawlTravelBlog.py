import logging
import LoggerConfig
import ElasticMappings
from TravelBlogParser import TravelBlogBlogParser, TravelPodAuthorParser,TravelBlogAuthorTripParser, TravelBlogMainSectionParser
import Util



def init ():
    ElasticMappings.Blog.init()
    ElasticMappings.Author.init()

class Crawler (object):#TODO: Refactor

    BASE_URL = "https://www.travelblog.org/Europe/Croatia/"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mainurl = self.BASE_URL + "blogs-page-16.html"
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

                        lastdate = self.currentblogparser.blog.postdate

                        while (currentauthorbloglisturl <> False):
                            authorblogparser = TravelBlogMainSectionParser(currentauthorbloglisturl)
                            authorblogparser.loaditem()

                            allauthorsurls = authorblogparser.parsebloglinks()
                            self.logger.info("No Trip Found, Parsing {0} ALL blogs for author: {1}".format(len(allauthorsurls),self.authorparser.author.username))
                            stopparsingauthor = False
                            for authorblog in allauthorsurls:
                                if self.__processblog(authorblog, False, self.isblogdatewithinrange, rangeofdate=lastdate) == False:
                                    stopparsingauthor = True
                                    break

                            if stopparsingauthor:
                                break

                            currentauthorbloglisturl = authorblogparser.getnext(self.authorparser.url)

                    self.authorparser.save()

            self.mainurl = sectionparser.getnext(self.BASE_URL)


    def __shouldcontinueparsingmain (self):
        return  self.mainurl <> False


    def isblogdatewithinrange (self, rangeofdate):
        result = Util.subtractdates(rangeofdate, self.currentblogparser.blog.postdate)
        if result  > 30:
            self.logger.info("blog isn't within 'trip' range of 30 days since last post")
            return False
        return True


    def __processblog (self, blogurl, resetauthor = False, customsavecheckfunction = None, **functionargs):

        self.currentblogparser = TravelBlogBlogParser(blogurl)

        try:
            didload = self.currentblogparser.loaditem(False)
        except:
            self.logger.exception("Couldn't load blog: {0}".format(self.currentblogparser.blog.url))
            return False

        if didload:
            try:
                self.currentblogparser.parseall()
            except:
                self.logger.exception("Couldn't parse blog: {0}".format(self.currentblogparser.blog.url))
                return False

            if resetauthor:
                self.authorparser = TravelPodAuthorParser(self.currentblogparser.getauthorurl())
                self.authorparser.loaditem()
                self.authorparser.parselogsummary()

            if customsavecheckfunction and customsavecheckfunction (**functionargs) == False:
                self.blogsparsed+=1
            elif self.currentblogparser.isvalidforindex():
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

