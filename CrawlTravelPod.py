import logging
import TravelPodParser
import ElasticMappings


def init ():
    ElasticMappings.Blog.init()
    ElasticMappings.Author.init()

def stopparsingcountry (blog):
    if blog.postdate.year < 2010:
        return True
    else:
        return False

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    init()

    countries = ['Uganda']
    number = 0
    for country in countries:

            for i in range(0,1000,1):

                mainurl = 'http://www.travelpod.com/blogs/{0}/{1}.html#'.format(i,country)
                mainSection = TravelPodParser.TravelPodMainSectionParser (mainurl)
                mainSection.loaditem()

                logger.info("Parsing Main Section: '{0}'".format(mainurl))
                blogs = mainSection.parsebloglinks();

                for blog in blogs:

                    currentblogparser = TravelPodParser.TravelPodBlogParser(blog)
                    if currentblogparser.loaditem(False):
                        currentblogparser.parseall()

                        if (stopparsingcountry(blog)):
                            continue

                        authorLink = currentblogparser.getauthorurl()
                        authorparser = TravelPodParser.TravelPodAuthorParser(authorLink)
                        authorparser.loaditem()
                        authorparser.parselogsummary()

                        if currentblogparser.isvalidforindex():
                            currentblogparser.blog.setauthor(authorparser.author)
                            currentblogparser.save()

                        authorparser.author.add_blog(currentblogparser.blog)
                        authorparser.save()

                        tripparser = TravelPodParser.TravelPodAuthorTripParser (currentblogparser.blog.trip)
                        tripparser.loaditem()
                        tripblogsurls = tripparser.parsebloglinks()

                        logger.info("Parsing {0} blogs for author: {1}".format(len(tripblogsurls),authorparser.author.username))

                        for blogurl in tripblogsurls[0:50]:
                            currentblogparser = TravelPodParser.TravelPodBlogParser('http://www.travelpod.com' + blogurl)
                            if currentblogparser.loaditem(False):
                                currentblogparser.parseall()

                                if (stopparsingcountry(blog)):
                                    continue

                                if currentblogparser.isvalidforindex():
                                    currentblogparser.blog.setauthor(authorparser.author)
                                    currentblogparser.save()

                                authorparser.author.add_blog(currentblogparser.blog)

                        authorparser.save()



