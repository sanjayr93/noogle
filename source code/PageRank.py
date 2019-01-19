# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

import numpy as np

class PageRank:
    def __init__(self):
        self.pages = set()
        self.adjList = {}
        self.prScores = {}
    
    def calculateScores(self, pages, d=0.85, maxiter=100):
        pages = sorted(list(pages))
        n = len(pages)
        A = np.zeros((n, n))
        # create the stochastic A matrix
        for node, adjNodes in self.adjList.items():
            row = pages.index(node)
            for aNode in adjNodes:
                try:
                    col = pages.index(aNode)
                    A[row, col] = 1
                except ValueError:
                    pass
        
        deno = np.sum(A, axis=1).reshape(n, 1)
        print(np.count_nonzero(deno))
        #out -> the output mat returned, wherever deno != 0 , the cells in that row are replaced by the division
        A = np.divide(A, deno, out=np.ones_like(A)*(1/n), where=deno!=0)
        scores = np.ones((n, 1)) * 1.0/n
        prev = np.zeros_like(scores)
        print("Starting pagerank iteration...")
        #power iteration
        iC = 0
        while np.linalg.norm(scores - prev, ord=1) != 0 and iC <= maxiter:
            prev = scores
            scores = (((1-d)/n) * np.ones((n, 1))) + np.matmul(d*A.T, prev)
            iC += 1
        print("Pagerank converged...")
        
        for i in range(n):
            self.prScores[pages[i]] = scores[i][0]