import re
import BeautifulSoup
from dateutil import parser
import Parser
import Util

class TravelBlogBlogParser(Parser.BlogParser):

    def parsemaincontent (self):
        rawbody = self.soup.find ('div', attrs={'class': re.compile('content')})

        postBodyText = ''
        for t in rawbody.contents:
            if type(t) is BeautifulSoup.NavigableString:
                postBodyText += t
            elif type(t) is BeautifulSoup.Tag and t.name == 'br':
                postBodyText += '\n'

        self.blog.body = postBodyText

        firstthumbnailimagediv = self.soup.find ('div', {"class":re.compile('photo-blog')})
        if (firstthumbnailimagediv):
            self.blog.thumbnailimage = 'https:' + firstthumbnailimagediv.findNext('img')['data-original']

        self.blog.title = self.soup.find("h1", {"class":"tb-banded"}).text

        strdate = self.soup.find('span', {'class':'blog-date'}).text
        self.blog.postdate =  parser.parse(strdate)

        picturedivs = self.soup.findAll('div', {'class': re.compile('photo-blog')})
        if (picturedivs):
            self.blog.photocount = len(picturedivs)

    def parselocation (self):

        locationStack = []
        locationdiv = self.soup.find('div', {'class':re.compile('country-info')})

        locationsibling = locationdiv.nextSibling
        while locationsibling != None:
            if type(locationsibling) is BeautifulSoup.Tag and locationsibling.name == 'a':
                locationStack.append(locationsibling.text.lower())
            locationsibling = locationsibling.nextSibling

        self.blog.city = ''
        self.blog.state = ''
        self.blog.country = ''

        if len(locationStack) >= 2 and len (locationStack) <=4:
            self.blog.country = locationStack[1]
            if len (locationStack) >= 3:
                self.blog.state = locationStack[2]
            if len (locationStack) == 4:
                self.blog.city = locationStack[3]
        else:
            raise NotImplementedError("Invalid Location")

        self.isafrica = locationStack[0].lower () == 'africa'

        if (self.isafrica == False):
            self.logger.info(self.blog.country + " is not an African country")

    def getauthorurl (self):
        authorhref = self.soup.find ('div', {'class':'article-head'}).findNext ('a')['href']
        authorlink = "http://www.travelblog.org" + authorhref
        return authorlink

    def parsetrip (self):
        tripanchor = self.soup.find ('a', {'title':'from trip...'})
        if tripanchor:
            self.blog.trip = "http://www.travelblog.org" + tripanchor['href']
        else:
            self.blog.trip = None
        return self.blog.trip

class TravelPodAuthorParser (Parser.AuthorParser):

    def parselogsummary (self):
        self.author.username = self.soup.find('h1', {'class':'tb-banded'}).text
        table = self.soup.find('table', {'class':'table'})
        rows = table.findAll('tr')
        for row in rows:
            cells = row.findAll ('td')
            if (cells[0].text == 'Blogs'):
                self.author.blogcount = cells[1].text
                break

        photodiv = self.soup.find('div', {'class':re.compile('photo')})
        self.author.photo = 'https:' + photodiv.find('img')['src']


class TravelBlogAuthorTripParser (Parser.Parser):
    def getitemid(self):
        return False

    def parsebloglinks (self):
        self.bloglist = []

        blogentrytable = self.soup.find('h2').nextSibling
        rows = blogentrytable.findAll('tr')
        for row in rows:
            cells = row.findAll ('td')
            if (len(cells) == 3):
                self.bloglist.append('http://www.travelblog.org' + cells[1].findNext ('a')['href'])

        return self.bloglist

class TravelBlogMainSectionParser (Parser.Parser):
    def getitemid(self):
        return False

    def parsebloglinks (self, addonlyenglish = False):
        self.bloglist = []

        leadingblogbrtags = self.soup.findAll('br', {'class':"blog-spacer"})
        for leadingblogbr in leadingblogbrtags:
            summary = leadingblogbr.nextSibling
            if addonlyenglish and Util.istextenglish(summary) == False:
                continue
            relativeurl = leadingblogbr.nextSibling.nextSibling['href']
            self.bloglist.append('http://www.travelblog.org' + relativeurl)

        return self.bloglist

    def getnext (self, baseurl):
        paginationlist = self.soup.find ('ul', {'class': 'pagination'})
        if paginationlist:
            listelements = paginationlist.findAll('li')
            if listelements and len(listelements) > 0:
                 href = listelements[len(listelements) - 1].find('a')['href']
                 if href== '#':
                     return False
                 return baseurl + href