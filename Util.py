import  uuid
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import chardet

def geturldata(url):
    result = urlopen(url)
    rawdata = result.read()
    encoding = chardet.detect(rawdata)
    return rawdata.decode(encoding['encoding'])

def generatebase64uuid():
    return uuid.uuid1().bytes.encode('base64').rstrip('=\n').replace('/', '_')

def uuidfrombase64string(string):
    return uuid.UUID(bytes=(string + '==').replace('_', '/').decode('base64'))
