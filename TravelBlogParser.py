import re
import BeautifulSoup
from dateutil import parser
import Parser

__author__ = 'trentniemeyer'


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
            self.blog.thumbnailimage = 'https:' + firstthumbnailimagediv.findNext('img')['src']

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
        return self.blog.trip