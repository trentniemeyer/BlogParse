import TravelPodParser
import json

if __name__ == '__main__':
    parser = TravelPodParser.BlogParser("http://www.travelpod.com/travel-blog-entries/bridie.sheehan/1/1433692810/tpod.html", False)
    parser.parseall()
    #print json.dumps(parser.data)
    #print json.dumps(parser.authorparser.data)
    print parser.authorparser.save()
    print parser.save()
