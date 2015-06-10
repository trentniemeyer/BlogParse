import TravelPodParser

if __name__ == '__main__':
    parser = TravelPodParser.BlogParser("http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html", False)
    parser.parseMainContent()
    parser.parseLocation()
    parser.parseAuthor()
    parser.saveBlogAndAuthor()