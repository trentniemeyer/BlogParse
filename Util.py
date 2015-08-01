from incf.countryutils import transformations
from contextlib import closing
import uuid
import urllib2

from elasticsearch_dsl.connections import connections
from azure.storage import BlobService
import langid
from PIL import Image
import io

# import nltk
# from nltk.tag.stanford import NERTagger

config = {
    'container': 'blogparsedev',       #blogparse or blogparsedev
    'eshost': 'localhost'           #localhost or 137.135.93.224
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

    bytes = io.BytesIO (urllib2.urlopen(url).read())
    img = Image.open(bytes)
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

        fp = io.BytesIO()
        newimg.save (fp, 'JPEG')
        bytes = fp.getvalue()

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
    try:
        if location.startswith('Congo'):
            return True
        return transformations.cn_to_ctn(location) == 'Africa'
    except:
        return False

#TODO: make NERTagger singleton variable.  load once.
# def nerlocationsandorganizations(text):
#     st = NERTagger("/Users/trentniemeyer/nltk_data/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz",
#        "/Users/trentniemeyer/nltk_data/stanford-ner-2014-06-16/stanford-ner.jar")
#     ne = st.tag(nltk.word_tokenize(text))
#     for sentence in ne:
#         for (word, entitytype) in sentence:
#             if entitytype == 'ORGANIZATION' or entitytype == 'LOCATION':
#                 print word + ":" + entitytype

