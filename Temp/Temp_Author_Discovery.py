# -*- coding: utf-8 -*
from elasticsearch import  Elasticsearch
import Util

from nltk.collocations import *
import nltk
import six

from nltk.corpus import stopwords
from gensim import corpora, models, similarities, summarization
from pprint import pprint

import LoggerConfig

country = "All"


def getblogs ():
    client = Elasticsearch([Util.config['eshost']])
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

def gensium_topic ():
    text = "Bit of a slacker today, getting up at 0615. Shower and still no wifi luck. The Algerian Committee was first down for brekkie, the Chancellor of the Exchequer joining. Omar said he had email.  I brought my computer to his [third] floor and it worked fine. It appeared there was no initial fifth floor connection but it worked thereafter having established a link. He showed me some pix of him and Ratik in Algiers. Took the bag down c 0830.Managed to upload the blog from two days ago. Went down after 0900 to see if I could help with the bags. Most people were on the bus at 0905, 25M early. Noubi expressed frustration thereon too. I did a bit more journal and headed down c 0920.Dumb Keith was greedily leaving his bag on a seat when the two bags Fashion Police and Eyesore were looking for seats. John was not surprised at the manners of his countryman. Wo(Man) and Helen of Troy are in the back seat so the yapping should be pretty constant today. Just because both of them don't like Noubi does not mean they should show a complete lack of courtesy and babble when he is on the microphone giving information.Sat with John and chatted about travel. He's been to the DMZ from the South Korean side. Three large phosphate fertilizer factories are on our distant left while we chat about his forthcoming Teheran-based trip to Iran. Olive groves predominate the country, some farms stretched out for kilometres on end.John and I have yet to figure out the import of the martini glass-looking part of some signage re pharmacies. I think it might be a stylized version of a cup of medicine, per the god Asclepius. Asked John if the attire of Eyesore was the BBC test pattern; he was not sure.As we zipped along Hwy 1 southbound, Noubi told us about olive production. Adult trees only need rain water to survive. Harvesting is started on Oct 15th for a particular corp; Nov 15th, for the main crop. The olives are removed from the trees by spreading out tarpaulines on the ground and the use of electrical vibrators to shake them off [or Helen of Troy, in a drunken stupor, just haphazardly crashes into the trees]. Tunisian olives are known for low acidity and a good for those with cholesterol issues.There were many jerry cans along the road. Drivers of oil tankers from Libya stop and make a bit of money by siphoning off some oil. The locals then resell it at a price still below the normal rates. While illegal, the government turns a blind eye to the practice as the area is poor.Chatted about my musings for a final trek. John is not a fan of trekking, finding the Inca Trail hard enough at 21.Stopped early for lunch near Skhira, at the junction of Hwys 1 and 2. Tony bought the espresso and I reciprocated re the calzone-type items . The Canadian Committee chowed down. Cora is somewhat dubious of Noubi, comparing him to her recent guide in Morocco. Tony called his not a leader but a mis-leader, a nice turn on words if nothing else. We might make John an honourary member of our committee as an expat.Noubi told Tony that Explore said he'd have to pay if he wanted the Hotel Majestic [even though already promised as an upgrade re tour changes] and then just get a credit re future travel re the already paid for Hotel El Pacha nights. That is crazy and not the way to treat somebody who has traveled 30+ times with Explore. Helen of Troy suggested a list be given to Noubi re issues; the idea is sound but will see if anybody actually does it.We were off at noon. Noubi gave us the drill about three options today and two days away. Today was a caleche or camel ride, going through Berber villages and seeing a sunset. The Gabes oasis is seven square kilometres and the country's only maritime oasis. It is known for its henna and pomegranate production.At Gabes at 1250 and walked through the spice market. Spices are always colourful. All the base henna is a pea green, later processing providing the reds, blacks, etc.After the tour Tony and I meandered. Somebody invited us inside his house as we wanted to take a picture of his exterior door. Exiting, we realized the house was attached to a mosque. Bearing in mind the chap's attire, he must have been an iman. It was a very nice gesture. Got some water  and off at 1340.I was making John laugh that Hugh was hitting on Fashion Police ie playing footsie, offering her his--actually a--banana. John and I continued to discuss travel; a safari does not turn his crank. Omar, Tony, Hugh and the Eyesore are doing today's option [30 TD]. Tony was out there with his money, ready to pay. Told John Omar had nicknamed Maggie May 'the Eyesore'. He chuckled but said that was cruel, the difference with North American humour. More people will do the jeep option later. Have to organize a 'party jeep'.Got to the Djerba ferry area after 1500. Noubi took a look at the queue--the longest he had ever seen but this is a holiday period--and decided it might be better to drive around to a causeway.God knows what stupid topic Hugh was talking about--I think it was the cost/benefit of gong by causeway--but he yapped about 'an interesting exercise in the logistics of reality'. He's a dumb bunny.Omar is working on more pins for his fez. We hit our last roundabout toward the causeway at 1600. A constant companion was two separate water lines to the island, one for the locals and one for the tourists. Noubi gave us some island stats, including the fact there were three principal towns.The present causeway is based on a Roman creation. It is some 4k long. The island is thought to be the Land of the Lotus Eaters, encountered by Odysseus on his return home from the Trojan War.Stopped for a loo/java break. A local football/soccer game was on the tube. John is an LFC fan, Roddy. It took ten minutes to cross the causeway. There were many resorts, akin to Cancun, Brys. As we were running late, we went directly to the caleche place, arriving at 1710. It was windy on the island. Stupid Hugh accidently kicked an adorable white, playful puppy.The Hotel Djerba Palace was huge and busy with a combination of locals and by and large French tourists. We had porters, placating some. There was only wifi in the lobby and even that was fleeting. Uploading pictures was a chore to impossible.The option people returned. Spoke briefly to Tony who was furious. All he wanted was just a hot shower. I suspect they were all very cold. Readied for dinner.Took a bus to La Paillote des Dunes. Ordered grilled calamari and got got a mixed grill. Had auburgine for a starter and a Celtia beer. The Fashion Police is boring dinner company but had fun with Omar and John. Background music was very western, including 'My Way'. There was a lounge singer whom the locals ignored. Paying the bill, I saw what I got was cheaper than what I ate so decided just to pay for that and a beer .Back at the hotel c 2245. Took the computer to reception. The wifi was operational but not functional. The locals use the reception area to convivialize rather than staying in their rooms, bearing in mind they do not drink. Frustrated, I gave up after 2330, bagging out before midnight."

    sentences = text.split(".")
    tokens = [sentence.split() for sentence in sentences]
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(sentence_tokens) for sentence_tokens in tokens]

    print(summarization.summarize(text))


#TODO:  Check these clustering samples:
        # http://stackoverflow.com/questions/6486738/clustering-using-latent-dirichlet-allocation-algo-in-gensim
        #http://www.williamjohnbert.com/2012/05/an-introduction-to-gensim-topic-modelling-for-humans/
        #http://brandonrose.org/clustering

#gensim_usage()
#gensim_partII()
gensium_topic()