# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

import pickle
import glob
from nltk.stem import PorterStemmer
import gensim
from Indexer import Index
from PreProcessor import PreProcessor
from QueryProcessor import QueryProcessor
from tkinter import *
from tkinter.messagebox import *


prScores = None
index = None
dataset = None
stemmer = PorterStemmer()
N = 0

print("Initializing PreProcessor...")
preprocessor = PreProcessor()

try:
	with open('pgrankscores', 'rb') as inf:
	    prScores = pickle.load(inf)
except:
	print("Please place the 'pgrankscores' pickle file in the same dir as this script or run runCrawler.py first to calculate the pagerank scores...")
	exit()

try:
	with open('index', 'rb') as indf:
	    index = pickle.load(indf)
	    N = index.N
except:
	print("Please place the 'index' pickle file in the same dir as this script...")

	print("Since there is no pre-computed index, do you want to rerun indexing ?")
	choice = input("CAUTION!!! Indexing can run for a few minutes! Also there should be a data folder with all the crawled files in this directory. Your choice ? (y/n) :")

	if choice == 'y':
		files = glob.glob('data/*')
		files = sorted(files)
		N = len(files)

		index = Index(N)
		# for topic modelling
		dataset = list()
		print("Indexing...")
		preprocessor.preprocess(files, [], index.updateIndex, dataset, stemmer=stemmer)
		index.computeDocLength()

		print("Pickling the index for future use...")
		with open('index', 'wb') as indf:
		    pickle.dump(index, indf)

		# with open('dataset', 'wb') as dsf:
		#     pickle.dump(dataset, dsf)
	else:
		exit()

print("Initializing the QueryProcessor...")
if dataset != None:
	print("Training the cluster model with", str(len(dataset)), "documents...")
	qProcessor = QueryProcessor(preprocessor, index=index, dataset=dataset)
	qProcessor.load_models()
	print("Saving the newly built models...")
	qProcessor.dictionary.save('ldaDict.gensim')
	qProcessor.lda_ti.save('lda_ti_model.gensim')
else:
	qProcessor = QueryProcessor(preprocessor, index=index, dataset=dataset)
	qProcessor.load_models()

def results(query, simChoice, page):
	print("\nPerforming search with only similarity measure...")
	result = qProcessor.getResults(query, wScheme=simChoice, stemmer=stemmer, page=page)

	print("Printing Results...")
	for i in result.items():
		print(i)

	print("\nPerforming search with similarity measure and pagerank...")
	resultRank = qProcessor.getResults(query, wScheme=simChoice, rankScheme=prScores, stemmer=stemmer, page=page)

	print("Printing Results...")
	for i in resultRank.items():
		print(i)

	print("\nPerforming search with similarity measure, pagerank and clustering...")
	clusterResult = qProcessor.getResults(query, wScheme=simChoice, rankScheme=prScores, stemmer=stemmer, qExpand=True, page=page)

	print("Printing Results...")
	for i in clusterResult.items():
		print(i)


print("\n Press '1' to start using Noogle command line UI - displays additional details \n Press '2' to start Noogle GUI")
flag = input("Your choice: ")
if flag == '1':
	while flag != 'n':
		query = input("Please enter a query: ")
		simChoice = input("Which similarity measure do you want to use (cosine -> cosSim, inner product -> innProd, dice -> dicSim, jaccard -> jacSim)? (case sensitive): ")

		page = -1
		cc = 'y'
		while cc != 'n':
			page += 1
			results(query, simChoice, page)
			cc = input("Go to next page ? (y/n): ")

		flag = input("Do you want to continue ? (y/n): ")

elif flag == '2':
	page = 0
	def show_answer():
		resultRank = qProcessor.getResults(queryBox.get(), wScheme=simC.get(), rankScheme=prScores, stemmer=stemmer, page=page)

		Ans = ""
		for i in resultRank.items():
			Ans += i[0] + "\n"

		resLabel['text'] = Ans

	def next_page():
		global page
		page += 1
		show_answer()

	main = Tk()
	Label(main, text = "Enter Query:").grid(row=0)
	Label(main,
	 text = "Similarity measures options - For cosine use cosSim, inner product -> innProd, dice -> dicSim, jaccard -> jacSim (case sensitive)").grid(row=1, columnspan=2)
	Label(main, text = "Enter similarity measure:").grid(row=2)
	resLabel = Label(main)
	resLabel.grid(row=3, columnspan=2, rowspan=10)


	queryBox = Entry(main)
	simC = Entry(main)
	
	queryBox.grid(row=0, column=1)
	simC.grid(row=2, column=1)

	Button(main, text='Search', command=show_answer).grid(row=15, column=0, sticky=W, pady=4)
	Button(main, text='Next Page', command=next_page).grid(row=15, column=1, sticky=W, pady=4)
	Button(main, text='Quit', command=main.destroy).grid(row=15, column=2, sticky=W, pady=4)

	mainloop()