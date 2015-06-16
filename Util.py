import  uuid
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import chardet
import boto
from elasticsearch_dsl.connections import connections
from boto.s3.key import Key

connections.create_connection(hosts=['localhost'])

def geturldata(url):
    result = urlopen(url)
    rawdata = result.read()
    encoding = chardet.detect(rawdata)
    return rawdata.decode(encoding['encoding'])

def generatebase64uuid():
    return uuid.uuid1().bytes.encode('base64').rstrip('=\n').replace('/', '_')

def uuidfrombase64string(string):
    return uuid.UUID(bytes=(string + '==').replace('_', '/').decode('base64'))

def putobjectins3 (strkey, data):
    connection = boto.connect_s3('AKIAIC6W4Q4N2DVAWLIQ', '8KiMgPLXvLaSRe8gRJNZvhowKoH2x0ReRPPM9xMh')
    bucket = connection.get_bucket('blogparse')
    s3key = Key(bucket)
    s3key.key = strkey
    s3key.set_contents_from_string(data)

def getobjectins3 (strkey):
    connection = boto.connect_s3('AKIAIC6W4Q4N2DVAWLIQ', '8KiMgPLXvLaSRe8gRJNZvhowKoH2x0ReRPPM9xMh')
    bucket = connection.get_bucket('blogparse')
    s3key = Key(bucket)
    s3key.key = strkey
    return s3key.get_contents_as_string()





