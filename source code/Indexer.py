# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

import math

class Index:
    def __init__(self, N):
        # inverted index, collection size and document length table
        self.index = {}
        self.N = N
        self.docLength = {}    
    
    # creates and updates the inverted index which is a map between tokens and a table of docId and the term frequency
    def updateIndex(self, docId, source: list):
        for word in source:
            docMap = self.index.get(word, {})
            docMap[docId] = docMap.get(docId, 0) + 1
            self.index[word] = docMap

    # Computes the sum of the squares of the term weights in the document vector
    # Sqrt of the sum should be computed while the individual values are used in future calculations
    def computeDocLength(self):
        for term, docMap in self.index.items():
            for docId, tf in docMap.items():
                length = self.docLength.get(docId, 0)
                length += math.pow(tf * math.log((self.N/len(docMap)), 2), 2)
                self.docLength[docId] = length

    # creates a map with tokens and their frequencies in the list
    def listToFreqDict(self, source: list):
        temp = {}
        for word in source:
            temp[word] = temp.get(word, 0) + 1
        return temp

    # - computes the cosine similarity between the query and the documents in the collection.
    # - computes the inner product as sum of partial terms iteratively and then divides the inner product by
    # the product of the sqrt of document and query length.
    # - Then the documents are sorted in descending order and the ranked list is returned.
    def cosineSimilarity(self, qTokens: list):
        cosSim = {}
        qLen = 0.0
        for token, qtf in self.listToFreqDict(qTokens).items():
            docMap = self.index.get(token)
            if docMap != None:
                qLen += math.pow(qtf * math.log((self.N/len(docMap)), 2), 2)
                for docId, tf in docMap.items():
                    value = cosSim.get(docId, 0)
                    value += (tf * qtf * math.pow(math.log((self.N/len(docMap)), 2), 2))
                    cosSim[docId] = value

        qLen = math.sqrt(qLen)
        for docId in cosSim.keys():
            cosSim[docId] = cosSim[docId] / (math.sqrt(self.docLength[docId]) * qLen)
        return cosSim
    
    def innerProduct(self, qTokens: list):
        innProd = {}
        for token, qtf in self.listToFreqDict(qTokens).items():
            docMap = self.index.get(token)
            if docMap != None:
                for docId, tf in docMap.items():
                    value = innProd.get(docId, 0)
                    value += (tf * qtf * math.pow(math.log((self.N/len(docMap)), 2), 2))
                    innProd[docId] = value
        return innProd
    
    def diceSimilarity(self, qTokens: list):
        dicSim = {}
        qLen = 0.0
        for token, qtf in self.listToFreqDict(qTokens).items():
            docMap = self.index.get(token)
            if docMap != None:
                qLen += math.pow(qtf * math.log((self.N/len(docMap)), 2), 2)
                for docId, tf in docMap.items():
                    value = dicSim.get(docId, 0)
                    value += (tf * qtf * math.pow(math.log((self.N/len(docMap)), 2), 2))
                    dicSim[docId] = value

        for docId in dicSim.keys():
            dicSim[docId] = (2 * dicSim[docId]) / (self.docLength[docId] + qLen)
        return dicSim
    
    def jaccardSimilarity(self, qTokens: list):
        jacSim = {}
        qLen = 0.0
        for token, qtf in self.listToFreqDict(qTokens).items():
            docMap = self.index.get(token)
            if docMap != None:
                qLen += math.pow(qtf * math.log((self.N/len(docMap)), 2), 2)
                for docId, tf in docMap.items():
                    value = jacSim.get(docId, 0)
                    value += (tf * qtf * math.pow(math.log((self.N/len(docMap)), 2), 2))
                    jacSim[docId] = value

        for docId in jacSim.keys():
            jacSim[docId] = jacSim[docId] / (self.docLength[docId] + qLen - jacSim[docId])
        return jacSim