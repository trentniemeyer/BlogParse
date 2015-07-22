# -*- coding: utf-8 -*
import logging

from elasticsearch import  Elasticsearch
import Util

from nltk.collocations import *
import nltk
import six

from simserver import SessionServer
from gensim import utils

from nltk.corpus import stopwords
from gensim import corpora, models, summarization, similarities
from pprint import pprint

import LoggerConfig
import Pyro4

country = "South Africa"
logger = logging.getLogger(__name__)


def getblogs ():
    client = Elasticsearch([Util.config['eshost']])

    response = client.search(
                index="blogs",
                body={
                    "size": "1000",
                    "query": {
                        "match": {
                          "country": country
                        }
                      }
                }
            )

    # response = client.search(
    #             index="blogs",
    #             body={
    #                 "size": "5000",
    #                 "query": {"match_all": {}}
    #             }
    #         )

    documents = []
    for hit in response['hits']['hits']:
        documents.append(hit["_source"]["body"])

    return  documents

def ntlk_usage ():

    documents = getblogs ()

    corpus = ''
    # for hit in response['hits']['hits']:
    #     corpus += hit["_source"]["body"]
    for blogtext in documents:
        corpus += blogtext

    stops = [unicode(word) for word in stopwords.words('english')] + ['re:', 'fwd:', '-']
    prime_words = [word for word in corpus.split() if word.lower() not in stops]

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    trigram_measures = nltk.collocations.TrigramAssocMeasures()

    # change this to read in your data
    finder = BigramCollocationFinder.from_words(prime_words)

    # only bigrams that appear 3+ times
    finder.apply_freq_filter(3)

    # return the 10 n-grams with the highest PMI
    #finder.nbest(bigram_measures.pmi, 10)

    for bigram in finder.score_ngrams(bigram_measures.raw_freq)[:10]:
        print bigram

    print '-----------------'

    for bigram in finder.nbest(bigram_measures.pmi, 5):
        print bigram

def gensim_usage ():

    documents = getblogs ()

    stops = [unicode(word) for word in stopwords.words('english')] + [u':-).', u'–', u'-', u'…', '!!!', '!!', 'x', 'got', 'get', 'went', 'us', u'I\'m']

    print stops

    texts = [[word for word in document.lower().split() if word not in stops]
              for document in documents]

    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
          for text in texts]

    # pretty-printer
    dictionary = corpora.Dictionary(texts)
    dictionary.save(country + '.dict')
    #print(dictionary.token2id)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(country + '.mm', corpus) # store to disk, for later use
    #print corpus

def gensim_partII():
    dictionary = corpora.Dictionary.load(country + '.dict')
    corpus = corpora.MmCorpus(country + '.mm')

    print corpus
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
    corpus_lsi = lsi[corpus_tfidf]
    print "LSI"
    lsi.print_topics(50)
    # for doc in corpus_lsi:
    #    print(doc)

    print "LDA"
    lda = models.LdaModel (corpus_tfidf, id2word=dictionary, num_topics=50)
    lda.print_topics(50)

    #print "HDP"
    #hdp = models.HdpModel(corpus, id2word=dictionary)
    #hdp.print_topics(10)

def gensim_topic ():
    text = "Saturday was a lot of journeying to get to the PangalaneLakes.  We took 2 taxi-brousse and then acar met us at the junction to Manambato to take us to our hotel’s boat.  The journey was very windy and sickening aswe travelled through the mountains and towards the coast.  We were met off the boat with a cocktail andsome snacks, a great start to a relaxing few days.The hotel lay on a strip of white sand between two lakes.  This meant you could watch both the sunriseand the sunset above the water.  Westayed in little bungalows along the beach and felt like we’d hired a privateisland as there were no other guests around. Matt went for a first dip in one of the lakes and emerged unscathed which was lucky considering we later found out that crocodiles had been spotted there.  The rest of us went swimming in the other lake which was safe!  Our versatile deckchairs helped with beach volleyball and football as well as reading in the sun.  In the evenings we watched the stars and drank cocktails by the fire we made.  Heavenly!There were two cheeky bamboo lemurs living on the strip thatoccasionally came around meal times to steal anything we’d left and they weren’tafraid of humans in the slightest.  After our chilled couple of days we hired a boat to take usto Tamatave along the lakes.  We stoppedfor a beautiful picnic on the beach half way through the journey and also gotto see one of the local villages when we had to stop to ask if I could usetheir loo!  Lots of men from the villageswere out fishing in their pirogues, made from hollowed out tree trunks."

    sentences = text.split(".")
    tokens = [sentence.split() for sentence in sentences]
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(sentence_tokens) for sentence_tokens in tokens]

    print(summarization.summarize(text))

def gensim_document_similarity ():
    #TODO: Try changing corpus to MalletCorpus so you can store document name and ID
    corpus = corpora.MmCorpus(country + '.mm')
    print corpus
    index = similarities.SparseMatrixSimilarity(corpus)

    for s in index:
        print s

def gensimsimserver ():
    server = SessionServer('myserver')
    texts = ["Human machine interface for lab abc computer applications",
          "A survey of user opinion of computer system response time",
          "The EPS user interface management system",
          "System and human system engineering testing of EPS",
          "Relation of user perceived response time to error measurement",
          "The generation of random binary unordered trees",
          "The intersection graph of paths in trees",
          "Graph minors IV Widths of trees and well quasi ordering",
          "Graph minors A survey"]
    corpus = [{'id': 'doc_%i' % num, 'tokens': utils.simple_preprocess(text)}
        for num, text in enumerate(texts)]
    server.train(corpus, method='lsi')
    server.index(corpus)
    print "********************************************"
    print(server.find_similar('doc_0'))

def gensimsimserverII ():

    reloadData = True
    useremoteserver = False

    if (useremoteserver):
        server = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
    else:
        server = SessionServer('/tmp/testserver') #SessionServer('myserver')


    if (reloadData):
        client = Elasticsearch([Util.config['eshost']])

        # response = client.search(
        #             index="blogs",
        #             body={
        #                 "size": "5000",
        #                 "query": {
        #                   "match": {
        #                     "country": country
        #                   }
        #                 }
        #             }
        #         )

        response = client.search(
                index="blogs",
                body={
                    "size": "5000",
                    "query": {"match_all": {}}
                }
            )

        stops = [unicode(word) for word in stopwords.words('english')] + [u':-).', u'–', u'-', u'…', '!!!', '!!', 'x', 'got', 'get', 'went', 'us', u'i\'m', '&', ]
        corpus = []
        for hit in response['hits']['hits']:
            try:
                body = hit["_source"]["body"]
                id = hit["_source"]["url"]
                title = hit["_source"]["title"]
                newBody = [word for word in body.lower().split() if word not in stops]

                corpus.append({
                    'id': id,
                    'tokens':newBody,
                    'title':title
                })

                server.stable.payload[id] = title

            except Exception:
                logger.exception("Couldn't parse blog id: {0}".format(hit["_id"]))

        server.train(corpus, method='lsi')
        server.index(corpus)

    print "********************************************"
    print(server.find_similar('http://www.travelpod.com/travel-blog-entries/bvrlymm/1/1428224775/tpod.html', max_results=5))

#TODO:  Check these clustering samples:
        # http://stackoverflow.com/questions/6486738/clustering-using-latent-dirichlet-allocation-algo-in-gensim
        #http://www.williamjohnbert.com/2012/05/an-introduction-to-gensim-topic-modelling-for-humans/
        #http://brandonrose.org/clustering

#gensim_usage()
#gensim_partII()
#gensium_topic()
#gensim_document_similarity ()

gensimsimserverII()