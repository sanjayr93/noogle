# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

from PageRank import PageRank
from NoogleSpider import NoogleSpider
import pickle

pagerank = None
spider = None
print("Reading PageRank object from prankNoScores...")
try:
	with open('prankNoScores', 'rb') as inf:
	    pagerank = pickle.load(inf)
except:
	print("ERROR---Please check if prankNoScores file is in the same directory as this script...")

	print("Since there is no pre-crawled data, do you want to crawl from the beginning ?")
	choice = input("CAUTION!!! Crawling can run for hours! Your choice ? (y/n) :")

	if choice == 'y':
		baseurl = input("Enter the start web-page to initiate crawl from (eg. https://www.cs.uic.edu) : ")
		maxP = int(input("Enter the max number of pages you want to try downloading: "))
		pagerank = PageRank()
		spider = NoogleSpider(baseurl, pagerank, maxPages=maxP)
		spider.crawl()

		print("Pickling the web structure as 'prankNoScores' file for future pagerank calculation...")
		with open('prankNoScores', 'wb') as outf:
		    pickle.dump(pagerank, outf)
	else:
		exit()

actPages = set(pagerank.adjList.keys())
tPages = pagerank.pages & actPages

flag = input("Do you want to run the pagerank iteration ? (y/n): ")
if flag == 'y':
	pagerank.calculateScores(tPages)

	print("Pickling the pagerank scores for using in index construction...")
	with open('pgrankscores', 'wb') as psf:
	    pickle.dump(pagerank.prScores, psf)
else:
	exit()