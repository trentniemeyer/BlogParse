from incf.countryutils import transformations
from contextlib import closing
import uuid
import urllib2
from datetime import datetime

from elasticsearch_dsl.connections import connections
from azure.storage import BlobService
import langid
from PIL import Image
import io

import nltk
from nltk.tag.stanford import NERTagger
import collections

config = {
    'container': 'blogparse',       #blogparse or blogparsedev
    'eshost': '137.135.93.224'           #localhost or 137.135.93.224
}

connections.create_connection(hosts=[config['eshost']])

def geturldata(url, cookiedict = None):

    opener = urllib2.build_opener()
    if cookiedict:
        for cookiename, cookievalue in cookiedict.items ():
            opener.addheaders.append(('Cookie', cookiename + '=' + cookievalue))

    with closing (opener.open(url)) as result:
        rawdata = result.read ()
        encoding = result.info().getparam("charset")
        return rawdata.decode (encoding)

def generatebase64uuid():
    return uuid.uuid1().bytes.encode('base64').rstrip('=\n').replace('/', '_')

def uuidfrombase64string(string):
    return uuid.UUID(bytes=(string + '==').replace('_', '/').decode('base64'))

def puttextobjectinazure (strkey, url, data):
    blob_service = BlobService(account_name='wanderight', account_key='gdmZeJOCx3HYlFPZZukUhHAfeGAu4cfHWGQZc3+HIpkBHjlznUDjhXMl5HWh5MgbjpJF09ZxRaET1JVF9S2MWQ==')
    blob_service.put_block_blob_from_text(
        config['container'], strkey, data,
        x_ms_meta_name_values={'url':url}
    )

def resizeimageandputinazure (strkey, url):
    maxwidthandheight = 150
    resize = False

    bytes = urllib2.urlopen(url).read()
    img = Image.open( io.BytesIO (bytes))
    newwidth = img.width
    newheight = img.height

    if (newheight > newwidth and newheight > maxwidthandheight):
        heightpercent = maxwidthandheight/float(newheight)
        newheight =  maxwidthandheight
        newwidth =  int((float(img.width)*float(heightpercent)))
        resize = True
    elif (newwidth > newheight and newwidth > maxwidthandheight):
        widthpercent = maxwidthandheight/float(newwidth)
        newwidth = maxwidthandheight
        newheight =  int((float(img.height)*float(widthpercent)))
        resize = True

    if resize:
        newimg = img.resize((newwidth, newheight), Image.ANTIALIAS)
        newimg.format = img.format

        newio = io.BytesIO()
        newimg.save (newio, 'JPEG')
        bytes = newio.getvalue()

    blob_service = BlobService(account_name='wanderight', account_key='gdmZeJOCx3HYlFPZZukUhHAfeGAu4cfHWGQZc3+HIpkBHjlznUDjhXMl5HWh5MgbjpJF09ZxRaET1JVF9S2MWQ==')
    blob_service.put_block_blob_from_bytes(config['container'], 'images/' + strkey, bytes,
                                           x_ms_blob_content_type='image/jpg', x_ms_meta_name_values={'url':url})


def gettextobjectfromazure (strkey):
    blob_service = BlobService(account_name='wanderight', account_key='gdmZeJOCx3HYlFPZZukUhHAfeGAu4cfHWGQZc3+HIpkBHjlznUDjhXMl5HWh5MgbjpJF09ZxRaET1JVF9S2MWQ==')
    return blob_service.get_blob_to_text(config['container'], strkey)

def deletefromazure (strPrefix):
    blob_service = BlobService(account_name='wanderight', account_key='gdmZeJOCx3HYlFPZZukUhHAfeGAu4cfHWGQZc3+HIpkBHjlznUDjhXMl5HWh5MgbjpJF09ZxRaET1JVF9S2MWQ==')
    blobsToDelete = blob_service.list_blobs(config['container'], prefix=strPrefix)
    for b in blobsToDelete:
        blob_service.delete_blob(config['container'], b.name)

def istextenglish (text):
    return langid.classify(text)[0] == 'en'

def isafrica (location):
    location = location.capitalize ()
    try:
        if location.startswith('Congo'):
            return True
        return transformations.cn_to_ctn(location) == 'Africa'
    except:
        return False

def subtractdates (datesooner, datelater):
    diff = datesooner - datelater
    return int(round(diff.total_seconds() /86400))

class NERParser (object):
    def __init__(self):
        self.st = NERTagger("/Users/trentniemeyer/nltk_data/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz",
            "/Users/trentniemeyer/nltk_data/stanford-ner-2014-06-16/stanford-ner.jar")
        self.locations = []
        self.organizations = []

    def parse (self, text):
        ne = self.st.tag(nltk.word_tokenize(text))
        for sentence in ne:
            lastwordwasentity = False
            lastentity = ''
            lasttype = ''
            for (word, entitytype) in sentence:
                if entitytype == 'ORGANIZATION' or entitytype == 'LOCATION':
                    if lastwordwasentity:
                        lastentity += ' ' + word
                    else:
                        lastentity = word
                    lastwordwasentity = True
                    lasttype = entitytype
                else:
                    if lastwordwasentity:
                        if lasttype == 'LOCATION':
                            self.locations.append(lastentity)
                        else:
                            self.organizations.append(lastentity)
                    lastentity = ''
                    lastwordwasentity = False

    def locationFrequencies (self):
        print collections.Counter (self.locations)

    def organizationFrequencies (self):
        print collections.Counter (self.organizations)