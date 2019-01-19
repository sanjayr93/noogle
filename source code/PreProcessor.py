# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

import string
from typing import Callable
from nltk.stem.api import StemmerI
from nltk.corpus import stopwords

# globals
#lets check how the results are when numbers are not removed in data and queries like courses,phone numbers,addresses
table = str.maketrans('', '', string.punctuation)# + "0123456789") 
table2 = str.maketrans('\\/-', '   ')

stopWords = set(stopwords.words('english'))

class PreProcessor:
    # tokenizes the text based on whitespaces, removes the punctuations and converts to lowercase
    # If a stemmer is passed, then stems the non stop-words as well
    def tokenize(self, file, target: list, stemmer: StemmerI=None):
        # stemmer is not gonna change within the loop so makes sense to do the check only once
        if stemmer is None:
            for line in file:
                # for stopwords - not anymore since we are using nltks stopwords
                line = line.translate(table2).strip()
                target.extend([word.lower() for word in line.translate(table).strip().split()
                               if (len(word) > 1 and
                                   word.lower() not in stopWords)])
        else:
            for line in file:
                # map() might look cleaner
                # for query
                line = line.translate(table2).strip()
                target.extend([stemmer.stem(word.lower()) for word in line.translate(table).strip().split() 
                               if (word.lower() not in stopWords and 
                                   stemmer.stem(word.lower()) not in stopWords and 
                                   len(word) > 1)])

    # function that tokenizes and constructs the vocabulary
    def preprocess(self, files, source: list, aggregator: Callable[..., None], dataset=None, stemmer: StemmerI=None):
        for i, file in enumerate(files):
            url = ''
            with open(file, 'r', encoding='ascii', errors='ignore') as f:
                url = f.readline().strip()
                self.tokenize(f, source, stemmer)
            aggregator(url, source)
            # for topic modelling, we need docs as list of tokens
            if dataset != None:
                dataset.append(source.copy())
            source.clear()