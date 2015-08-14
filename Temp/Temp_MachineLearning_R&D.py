# -*- coding: utf-8 -*
import logging

from elasticsearch import  Elasticsearch
import Util

from nltk.collocations import *
import nltk
from nltk.stem.snowball import SnowballStemmer
import six
import re

from simserver import SessionServer
from gensim import utils

from nltk.corpus import stopwords
from gensim import corpora, models, summarization, similarities
from pprint import pprint

import LoggerConfig
import Pyro4

country = "uganda" #South Africa, morocco, ALL
logger = logging.getLogger(__name__)

# https://github.com/cleder/restsims/blob/master/restsims/utils.py

def longstopwords ():#http://www.ranks.nl/stopwords
    return ['a','able','about','above','abst','accordance','according','accordingly','across','act','actually','added','adj','affected','affecting','affects','after','afterwards','again','against','ah','all','almost','alone','along','already','also','although','always','am','among','amongst', 'an', 'an\n','and','announce','another','any','anybody','anyhow','anymore','anyone','anything','anyway','anyways','anywhere','apparently','approximately','are','aren','arent','arise','around','as','aside','ask','asking','at','auth','available','away','awfully','b','back','be','became','because','become','becomes','becoming','been','before','beforehand','begin','beginning','beginnings','begins','behind','being','believe','below','beside','besides','between','beyond','biol','both','brief','briefly','but','by','c','ca','came','can','cannot','can\'t','cause','causes','certain','certainly','co','com','come','comes','contain','containing','contains','could','couldnt','d','date','did','didn\'t','different','do','does','doesn\'t','doing','done','don\'t','down','downwards','due','during','e','each','ed','edu','effect','eg','eight','eighty','either','else','elsewhere','end','ending','enough','especially','et','et-al','etc','even','ever','every','everybody','everyone','everything','everywhere','ex','except','f','far','few','ff','fifth','first','five','fix','followed','following','follows','for','former','formerly','forth','found','four','from','further','furthermore','g','gave','get','gets','getting','give','given','gives','giving','go','goes','gone','got','gotten','h','had','happens','hardly','has','hasn\'t','have','haven\'t','having','he','hed','hence','her','here','hereafter','hereby','herein','heres','hereupon','hers','herself','hes','hi','hid','him','himself','his','hither','home','how','howbeit','however','hundred','i','id','ie','if','i\'ll','im','immediate','immediately','importance','important','in','inc','indeed','index','information','instead','into','invention','inward','is','isn\'t','it','itd','it\'ll','its','it\'s',u'it’s', 'itself','i\'ve','i\'m',u'i’m', 'j','just','k','keep	keeps','kept','kg','km','know','known','knows','l','largely','last','lately','later','latter','latterly','least','less','lest','let','lets','like','liked','likely','line','little','\'ll','look','looking','looks','ltd','m','made','mainly','make','makes','many','may','maybe','me','mean','means','meantime','meanwhile','merely','mg','might','million','miss','ml','more','moreover','most','mostly','mr','mrs','much','mug','must','my','myself','n','na','name','namely','nay','nd','near','nearly','necessarily','necessary','need','needs','neither','never','nevertheless','new','next','nine','ninety','no','nobody','non','none','nonetheless','noone','nor','normally','nos','not','noted','nothing','now','nowhere','o','obtain','obtained','obviously','of','off','often','oh','ok','okay','old','omitted','on','once','one','ones','only','onto','or','ord','other','others','otherwise','ought','our','ours','ourselves','out','outside','over','overall','owing','own','p','page','pages','part','particular','particularly','past','per','perhaps','placed','please','plus','poorly','possible','possibly','potentially','pp','predominantly','present','previously','primarily','probably','promptly','proud','provides','put','q','que','quickly','quite','qv','r','ran','rather','rd','re','readily','really','recent','recently','ref','refs','regarding','regardless','regards','related','relatively','research','respectively','resulted','resulting','results','right','run','s','said','same','saw','say','saying','says','sec','section','see','seeing','seem','seemed','seeming','seems','seen','self','selves','sent','seven','several','shall','she','shed','she\'ll','shes','should','shouldn\'t','show','showed','shown','showns','shows','significant','significantly','similar','similarly','since','six','slightly','so','some','somebody','somehow','someone','somethan','something','sometime','sometimes','somewhat','somewhere','soon','sorry','specifically','specified','specify','specifying','still','stop','strongly','sub','substantially','successfully','such','sufficiently','suggest','sup','sure	t','take','taken','taking','tell','tends','th','than','thank','thanks','thanx','that','that\'ll','thats','that\'ve','the','their','theirs','them','themselves','then','thence','there','thereafter','thereby','thered','therefore','therein','there\'ll','thereof','therere','theres','thereto','thereupon','there\'ve','these','they','theyd','they\'ll','theyre','they\'ve','think','this','those','thou','though','thoughh','thousand','throug','through','throughout','thru','thus','til','tip','to','together','too','took','toward','towards','tried','tries','truly','try','trying','ts','twice','two','u','un','under','unfortunately','unless','unlike','unlikely','until','unto','up','upon','ups','us','use','used','useful','usefully','usefulness','uses','using','usually','v','value','various','\'ve','very','via','viz','vol','vols','vs','w','want','wants','was','wasnt','way','we','wed','we\'d', 'we\'re', 'welcome','we\'ll','went','were','werent','we\'ve','what','whatever','what\'ll','whats','when','whence','whenever','where','whereafter','whereas','whereby','wherein','wheres','whereupon','wherever','whether','which','while','whim','whither','who','whod','whoever','whole','who\'ll','whom','whomever','whos','whose','why','widely','willing','wish','with','within','without','wont','words','world','would','wouldnt','www','x','y','yes','yet','you','youd','you\'ll','your','youre','yours','yourself','yourselves','you\'ve','z','zero']

def testprocess (doc, deacc=True, lowercase=True, errors="strict"):
    stemmer = SnowballStemmer("english")
    for token in utils.tokenize(doc, lowercase=lowercase, deacc=deacc, errors=errors):
        yield stemmer.stem(token)

def simple_preprocess(doc, deacc=True, lowercase=True, errors='ignore',stopwords=longstopwords()):

    if not stopwords:
        stopwords = []

    for token in testprocess(doc, lowercase=lowercase, deacc=deacc, errors=errors):
        if 2 <= len(token) <= 25 and not token.startswith(u'_') and token not in stopwords:
            yield token.encode('utf8')

SPLIT_SENTENCES = re.compile(u"[.!?:]\s+")  # split sentences on '.!?:' characters

def bigram_preprocess(doc, deacc=True, lowercase=True, errors='ignore'):

    bigrams = []
    #split doc into sentences
    for sentence in SPLIT_SENTENCES.split(doc):
        #split sentence into tokens
        tokens = list(simple_preprocess(sentence, deacc, lowercase, errors=errors))
        #construct bigrams from tokens
        if len(tokens) >1:
            for i in range(0,len(tokens)-1):
                yield tokens[i] + '_' + tokens[i+1]

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
    #                 "size": "9000",
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

    stops = longstopwords() + [u':-).', u'–', u'-', u'…', '!!!', '!!', 'x', '&', '*', '.']
    prime_words = [word for word in corpus.split() if word.lower() not in stops]

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    trigram_measures = nltk.collocations.TrigramAssocMeasures()

    # change this to read in your data
    finder = BigramCollocationFinder.from_words(prime_words)
    finderII = TrigramCollocationFinder.from_words(prime_words)

    # only bigrams that appear 3+ times
    finder.apply_freq_filter(3)
    finderII.apply_freq_filter(3)

    # return the 10 n-grams with the highest PMI
    #finder.nbest(bigram_measures.pmi, 10)

    for bigram in finder.score_ngrams(bigram_measures.raw_freq)[:30]:
        print bigram

    print '-----------------'

    for trigram in finderII.score_ngrams(trigram_measures.raw_freq)[:30]:
        print trigram

def gensim_usage ():

    documents = getblogs ()

    #stops = longstopwords() + [u':-).', u'–', u'-', u'…', '!!!', '!!', 'x', '&', '*', '.']

    #     corpus += hit["_sourcev"]["body"]

    texts = [[word for word in simple_preprocess (doc)]
              for doc in documents]

    import operator
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    #sorted_frequency = sorted(frequency.items(), key=operator.itemgetter(1), reverse=True)

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

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50, extra_samples=None, power_iters=100)
    corpus_lsi = lsi[corpus_tfidf]

    print "LSI"
    # topics =  lsi.show_topics (num_topics=50, log=False, formatted=False)
    # for topic in topics:
    #      print [word[1] for word in topic]

    lsi.print_topics(50)

    # print "LDA"
    # lda = models.LdaModel (corpus_tfidf, id2word=dictionary, num_topics=50, passes=50)
    # lda.print_topics(50)

    # lda2 = models.LdaModel (corpus, id2word=dictionary, num_topics=30, passes=50)
    # lda2.print_topics(30)

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

        stops = [unicode(word) for word in stopwords.words('english')] + [u':-).', u'–', u'-', u'…', '!!!', '!!', 'x', 'got', 'get', 'went', 'us', u'i\'m', '&','it\'s', 'i\'ve' ]
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

#ntlk_usage()

#gensim_usage()
gensim_partII()
#gensium_topic()
#gensim_document_similarity ()