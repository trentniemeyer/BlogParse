from incf.countryutils import transformations
from contextlib import closing
import uuid
import urllib2

from elasticsearch_dsl.connections import connections
from azure.storage import BlobService
import langid

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

def copywebimageandputinazure (strkey, url):
    blob_service = BlobService(account_name='wanderight', account_key='gdmZeJOCx3HYlFPZZukUhHAfeGAu4cfHWGQZc3+HIpkBHjlznUDjhXMl5HWh5MgbjpJF09ZxRaET1JVF9S2MWQ==')
    buf = urllib2.urlopen(url).read()
    blob_service.put_block_blob_from_bytes(config['container'], 'images/' + strkey, buf,
                                           x_ms_blob_content_type='image/jpg', x_ms_meta_name_values={'url':url}
    )

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

def isafrica (locaion):
    try:
        return transformations.cn_to_ctn(locaion) == 'Africa'
    except:
        return False

