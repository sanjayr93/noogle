# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran

Setup steps:
- The search engine application requires the following modules - gensim, nltk, nltk english corpus, numpy, urllib, ssl, html
- Place the pickle files and the source codes from the source code directory together in the same target directory
- Run 'runCrawler.py' only if you want crawl from the beginning. If so, please do not forget to create an empty directory named "data".
- Otherwise, all the required objects have been pickled and 'main.py' will automatically read those files and reconstruct 
the objects (CAUTION!!! Crawling can run for hours...)
- Run 'main.py' and just follow the instructions