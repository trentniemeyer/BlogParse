import TravelPodParser
import time
import Util

if __name__ == '__main__':

    blogs = []

    currentblogparser = TravelPodParser.BlogParser("http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html", False)
    currentblogparser.parseall()

    authorLink = currentblogparser.getauthorurl()
    authorparser = TravelPodParser.AuthorParser (authorLink, False)
    authorparser.parselogsummary()

    authorid = Util.generatebase64uuid()
    author = authorparser.data
    author['id'] = authorid

    currentblogparser.blog.setauthor(author)
    currentblogparser.blog.save(html = currentblogparser.html)
    #blogs.append(currentblogparser.data)

    # tripparser = TravelPodParser.AuthorTripParser ("http://www.travelpod.com/travel-blog/bridie.sheehan/1/tpod.html")
    # tripblogsurls = tripparser.parsebloglinks()

    # answer = raw_input("You are about to parse %d which may spike or DOS their servers. type 'y' continue" % len (tripblogsurls))
    #
    # if answer == 'y':
    #     for blogurl in tripblogsurls:
    #         currentblogparser = TravelPodParser.BlogParser('http://www.travelpod.com' + blogurl, False)
    #         currentblogparser.parseall()
    #         currentsavedblog = currentblogparser.save(author)
    #         currentblogparser.data['id'] = currentsavedblog['_id']
    #         blogs.append(currentblogparser.data)

    #print authorparser.save(blogs)
