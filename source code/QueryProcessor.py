# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

from collections import OrderedDict
import gensim
from nltk.stem.api import StemmerI
import pickle
from pathlib import Path

class QueryProcessor:
    def __init__(self, preprocessor, index=None, dataset=None):
        self.preprocessor = preprocessor
        self.dataset = dataset
        if index != None:
            self.index = index
        else:
            try:
                with open('index', 'rb') as indf:
                    self.index = pickle.load(indf)
            except:
                print("Please place the index pickle file in the same dir as this script or else run indexing first...")
                exit()
    
    def load_models(self):
        if self.dataset != None:
            print("Building the cluster models...")
            self.dictionary = gensim.corpora.Dictionary(self.dataset)
            self.dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=15000)
            bow_corpus = [self.dictionary.doc2bow(doc) for doc in self.dataset]
            tfidf = gensim.models.TfidfModel(bow_corpus)
            corpus_tfidf = tfidf[bow_corpus]
            self.lda_ti = gensim.models.LdaModel(corpus_tfidf, num_topics=20, id2word=self.dictionary, passes=15)
        else:
            print("Loading model from pickles...")
            dictFile = Path('ldaDict.gensim')
            modelFile = Path('lda_ti_model.gensim')
            if dictFile.is_file() and modelFile.is_file():
                self.dictionary = gensim.corpora.Dictionary.load('ldaDict.gensim')
                self.lda_ti = gensim.models.ldamodel.LdaModel.load('lda_ti_model.gensim')
            else:
                print("Please place the gensim model pickles along with the script or else build the models again...")
                exit()

    def getResults(self, query, wScheme='cosSim', rankScheme=None, stemmer: StemmerI=None, qExpand=False, page=0):
        result = OrderedDict()
        qTokens = []        
        self.preprocessor.tokenize([query], qTokens, stemmer=stemmer)
        if qExpand:
            qCorpus = self.dictionary.doc2bow(qTokens)
            qTopic = sorted(self.lda_ti.get_document_topics(qCorpus), key=lambda t: -1*t[1])[0]
            newQTerms = [w[0] for w in self.lda_ti.show_topic(qTopic[0], topn=5)]
            qTokens.extend(newQTerms)
            print("The Expanded query is", ' '.join(qTokens))
            
        simScore = None
        if wScheme == 'cosSim':
            simScore = self.index.cosineSimilarity(qTokens)
        elif wScheme == 'innProd':
            simScore = self.index.innerProduct(qTokens)
        elif wScheme == 'dicSim':
            simScore = self.index.diceSimilarity(qTokens)
        elif wScheme == 'jacSim':
            simScore = self.index.jaccardSimilarity(qTokens)
        else:
            print("Invalid Similarity Measure...")
            return result
        
        if rankScheme:
            result.update(sorted(simScore.items(), key = lambda t: -1*t[1]))
            items = list(result.items())[10*page:10*(page+1)]
            result.clear()
            result.update(sorted(items, key = lambda t: -1*(2*t[1]*rankScheme[t[0]])/(t[1] + rankScheme[t[0]])))
        else:
            result.update(sorted(list(simScore.items()), key = lambda t: -1*t[1])[10*page:10*(page+1)])
        return result