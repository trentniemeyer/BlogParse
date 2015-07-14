# -*- coding: utf-8 -*
from elasticsearch import  Elasticsearch
import Util

from nltk.collocations import *
import nltk

from nltk.corpus import stopwords
from gensim import corpora, models, similarities
from pprint import pprint

import LoggerConfig

client = Elasticsearch([Util.config['eshost']])
country = "All"
#
# response = client.search(
#             index="blogs",
#             body={
#                 "size": "1000",
#                 "query": {
#                     "match": {
#                       "country": country
#                     }
#                   }
#             }
#         )

response = client.search(
            index="blogs",
            body={
                "size": "5000",
                "query": {"match_all": {}}
            }
        )

def ntlk_usage ():
    corpus = ''
    for hit in response['hits']['hits']:
        corpus += hit["_source"]["body"]

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

    documents = []
    for hit in response['hits']['hits']:
        documents.append(hit["_source"]["body"])

    stops = [unicode(word) for word in stopwords.words('english')] + [u':-).', u'–', u'-']

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
    #corpus_lsi = lsi[corpus_tfidf]
    print "LSI"
    lsi.print_topics(50)
    #for doc in corpus_lsi:
    #    print(doc)

    #print "LDA"
    #lda = models.LdaModel (corpus, id2word=dictionary, num_topics=10)
    #lda.print_topics(10)

    #print "HDP"
    #hdp = models.HdpModel(corpus, id2word=dictionary)
    #hdp.print_topics(10)

#TODO:  Check these clustering samples:
        # http://stackoverflow.com/questions/6486738/clustering-using-latent-dirichlet-allocation-algo-in-gensim
        #http://www.williamjohnbert.com/2012/05/an-introduction-to-gensim-topic-modelling-for-humans/
        #http://brandonrose.org/clustering

#gensim_usage()
gensim_partII()
