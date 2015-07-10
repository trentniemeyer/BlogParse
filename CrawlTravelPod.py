import TravelPodParser
import LoggerConfig
import logging
import ElasticMappings

def init ():
    ElasticMappings.Blog.init()
    ElasticMappings.Author.init()

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    init()

    countries = [('Kenya', 5),('Morocco', 5), ('Uganda',3), ('Zimbabwe',3)  ,('Ghana',3) ,('Mauritius', 1)]
    for (country, number) in countries:

        for i in range(0,number,1):

            mainurl = 'http://www.travelpod.com/blogs/{0}/{1}.html#'.format(i,country)
            mainSection = TravelPodParser.MainSectionParser (mainurl)
            mainSection.loaditem()

            logger.info("Parsing Main Section: '{0}'".format(mainurl))
            blogs = mainSection.parsebloglinks();

            for blog in blogs:
                #blog = "http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html"

                currentblogparser = TravelPodParser.BlogParser(blog)
                if (currentblogparser.loaditem(False)):
                    currentblogparser.parseall()

                    authorLink = currentblogparser.getauthorurl()
                    authorparser = TravelPodParser.AuthorParser (authorLink)
                    authorparser.loaditem()
                    authorparser.parselogsummary()

                    if (currentblogparser.isafrica):
                        currentblogparser.blog.setauthor(authorparser.author)
                        currentblogparser.save()

                    authorparser.author.add_blog(currentblogparser.blog)
                    authorparser.save()

                    tripparser = TravelPodParser.AuthorTripParser (currentblogparser.blog.trip)
                    tripparser.loaditem()
                    tripblogsurls = tripparser.parsebloglinks()

                    logger.info("Parsing {0} blogs for author: {1}".format(len(tripblogsurls),authorparser.author.username))

                    for blogurl in tripblogsurls[0:50]:
                        currentblogparser = TravelPodParser.BlogParser('http://www.travelpod.com' + blogurl)
                        if (currentblogparser.loaditem(False)):
                            currentblogparser.parseall()

                            if (currentblogparser.isafrica):
                                currentblogparser.blog.setauthor(authorparser.author)
                                currentblogparser.save()

                            authorparser.author.add_blog(currentblogparser.blog)

                    authorparser.save()



