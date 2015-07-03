import TravelPodParser
import LoggerConfig
import logging

if __name__ == '__main__':

    logger = logging.getLogger(__name__)

    mainSection = TravelPodParser.MainSectionParser ('http://www.travelpod.com/blogs/0/Africa.html#')
    blogs = mainSection.parsebloglinks();

    for blog in blogs:
        #blog = "http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html"

        currentblogparser = TravelPodParser.BlogParser(blog)
        currentblogparser.parseall()

        authorLink = currentblogparser.getauthorurl()
        authorparser = TravelPodParser.AuthorParser (authorLink)
        authorparser.parselogsummary()

        if (currentblogparser.isafrica):
            currentblogparser.blog.setauthor(authorparser.author)
            currentblogparser.save()

        authorparser.author.add_blog(currentblogparser.blog)
        authorparser.save()

        tripparser = TravelPodParser.AuthorTripParser (currentblogparser.blog.trip)
        tripblogsurls = tripparser.parsebloglinks()

        logger.info("Parsing {0} blogs for author: {1}".format(len(tripblogsurls),authorparser.author.username))

        for blogurl in tripblogsurls:
            currentblogparser = TravelPodParser.BlogParser('http://www.travelpod.com' + blogurl)
            currentblogparser.parseall()

            if (currentblogparser.isafrica):
                currentblogparser.blog.setauthor(authorparser.author)
                currentblogparser.save()

            authorparser.author.add_blog(currentblogparser.blog)

        authorparser.save()