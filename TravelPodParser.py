import re

from datetime import datetime
import BeautifulSoup

import Parser
import Util
import ElasticMappings

class TravelPodBlogParser (Parser.BlogParser):

    def parsemaincontent (self):
        postBody = self.soup.find(id="post")

        postBodyText = ''

        for t in postBody.contents:
            if type(t) is BeautifulSoup.NavigableString:
                postBodyText += t

        firstthumbnailimagediv = self.soup.find('div',  attrs={'class':re.compile('^inline-thumb')})

        if (firstthumbnailimagediv):
            thumbnailimage = firstthumbnailimagediv.findNext('img')['src']
            thumbnailimage = thumbnailimage.replace ("xlarge", "large")
            self.blog.thumbnailimage = thumbnailimage

        self.blog.body = postBodyText
        self.blog.title = self.soup.find("meta", {"name": "twitter:name"})['content']

    def parselocation(self):
        locationStack = []
        titleContents = self.soup.find("p", attrs={'class' : 'meta'}).contents
        for t in titleContents:
            if type(t) is BeautifulSoup.Tag:
                if t.name == 'a':
                    locationStack.append(t.string)
                elif t.name == 'span':
                    self.blog.postdate = datetime.strptime(t.string, '%A, %B %d, %Y')

        self.blog.city = ''
        self.blog.state = ''
        self.blog.country = ''
        if (len(locationStack) == 3):
            self.blog.country = locationStack[2]
            self.blog.state = locationStack[1]
            self.blog.city = locationStack[0]
        elif (len(locationStack) == 2):
            self.blog.country = locationStack[1]
            self.blog.state = locationStack[0]
        else:
            raise NotImplementedError("Single location field not handled yet")

        self.isafrica = Util.isafrica(self.blog.country)

        if (self.isafrica == False):
            self.logger.info(self.blog.country + " is not an African country")

    def getauthorurl (self):
        authorHref = self.soup.find("div", attrs={'class':'profile'}).findNext ('a')['href']
        authorLink = "http://www.travelpod.com" + authorHref
        return authorLink

    def parsetrip (self):
        self.blog.trip = 'http://www.travelpod.com' + self.soup.find("a", attrs={'title' : 'See more entries in this travel blog'})['href']

class TravelPodAuthorParser (Parser.AuthorParser):

    def parselogsummary (self):
        self.author.username = self.soup.find("meta", {"property":"og:title"})['content']
        summary = self.soup.find("div", attrs={'class' : 'bubble'}).contents
        for t in summary:
            if type(t) is BeautifulSoup.Tag:
                if t.name == 'span':
                    blogcount = str(t.string).split(' ')[0]
                    self.author.blogcount = blogcount.translate(None, ",")
        self.author.photo = self.soup.find(id="profile_pic")['src']

class AuthorTripParser (Parser.Parser):
    def getitemid(self):
        return False

    def parsebloglinks (self):
        self.bloglist = []
        for div in self.soup.findAll("div", {"class":"blog_data"}):
            self.bloglist.append(div.contents[1]['href'])
        return self.bloglist

class MainSectionParser (Parser.Parser):
    def getitemid(self):
        return False

    def loaditem(self, forcereindex = True, cookiedict = None):
        cookiedict = {'tweb_order':'time'} #sort by time so we can parse latest first (instead of most popular)
        Parser.loaditem(self,forcereindex, cookiedict)

    def parsebloglinks (self):
        self.bloglist = []
        for div in self.soup.findAll('div',  attrs={'class':re.compile('^blog_info$')}):
            if (Util.istextenglish(div.findAll('p')[1].text)):
                self.bloglist.append(div.findNext ('a')['href']);
        return self.bloglist

