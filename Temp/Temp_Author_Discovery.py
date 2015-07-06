from elasticsearch import  Elasticsearch
import Util

from nltk.collocations import *
import nltk

from nltk.corpus import stopwords
from gensim import corpora, models, similarities
from pprint import pprint

client = Elasticsearch([Util.config['eshost']])

response = client.search(
            index="blogs",
            body={
                "size": "30",
                "query": {
                    "nested": {
                      "path": "author",
                      "query": {
                        "match": {
                          "author.username": "Hippler"
                        }
                      }
                    }
                  }
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


def genism_usage ():

    documents = []
    for hit in response['hits']['hits']:
        documents.append(hit["_source"]["body"])

    stops = [unicode(word) for word in stopwords.words('english')] + ['re:', 'fwd:', '-']
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
    print(dictionary.token2id)

genism_usage()