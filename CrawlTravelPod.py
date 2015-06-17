import TravelPodParser
import time
import Util

if __name__ == '__main__':

    currentblogparser = TravelPodParser.BlogParser("http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html", False)
    currentblogparser.parseall()

    authorLink = currentblogparser.getauthorurl()
    authorparser = TravelPodParser.AuthorParser (authorLink, False)
    authorparser.parselogsummary()

    currentblogparser.blog.setauthor(authorparser.author)
    currentblogparser.save()

    authorparser.author.add_blog(currentblogparser.blog)
    authorparser.save()

    tripparser = TravelPodParser.AuthorTripParser (currentblogparser.blog.trip)
    tripblogsurls = tripparser.parsebloglinks()

    answer = raw_input("You are about to parse %d which may spike or DOS their servers. type 'y' continue" % len (tripblogsurls))

    if answer == 'y':
        for blogurl in tripblogsurls:
            currentblogparser = TravelPodParser.BlogParser('http://www.travelpod.com' + blogurl, False)
            currentblogparser.parseall()

            currentblogparser.blog.setauthor(authorparser.author)
            currentblogparser.save()
            authorparser.author.add_blog(currentblogparser.blog)

        authorparser.save()