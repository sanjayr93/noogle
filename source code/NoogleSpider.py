# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

from NoogleHTMLParser import NoogleHTMLParser
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib import robotparser
from urllib.error import URLError
from ssl import SSLError, CertificateError
import time

domainRules = {}

class NoogleSpider:
    def __init__(self, url: str, pgrank, maxPages=3000, name='*', htmlparser=None):
        self.maxPages = maxPages
        self.pgCount = 0
        self.linkQ = [[url, '']]
        self.linkSet = set()
        self.addToLinkSet(url.split("://")[1])
        self.htmlparser = htmlparser if htmlparser else NoogleHTMLParser()
        self.name = name
        self.rankScheme = pgrank

    def addToLinkSet(self, ll):
        if 'www.' in ll:
            self.linkSet.add(ll[4:])
        else:
            self.linkSet.add('www.' + ll)
        self.linkSet.add(ll)

    def crawl(self):
        print("Crawling Started...")
        lcount = 0
        while self.pgCount <= self.maxPages and len(self.linkQ) != 0:
            #print("Page-", self.pgCount)
            url = self.linkQ.pop(0)
            if self.crawl_allowed(url[0]):
                def link_canon(url):
                    url[0] = url[0].strip()
                    pr = urlparse(url[0])
                    # canonicalize the url
                    # remove #author kind of self refs
                    if len(pr.fragment) > 0:
                        url[0] = url[0].rsplit('#', maxsplit=1)[0]
                    # remove the ending /
                    if url[0].endswith('/'):
                        url[0] = url[0].rstrip('/')
                    return url
                
                links = list(map(link_canon, self.htmlparser.get_links(url)))

                adjPs = self.rankScheme.adjList.get(url[0], set())

                for link in links.copy():
                    if ('http://' in link[0] or 'https://' in link[0]) and 'uic.edu' in urlparse(link[0]).netloc:
                        ll = link[0].split("://")[1].strip()

                        if ".pdf" not in ll and ".xml" not in ll:
                            self.rankScheme.pages.add(link[0])
                            adjPs.add(link[0])
                            if ll not in self.linkSet:
                                self.addToLinkSet(ll)
                            else:
                                links.remove(link)
                        else:
                            links.remove(link)
                    else:
                        links.remove(link)

                self.rankScheme.adjList[url[0]] = adjPs

                if lcount <= self.maxPages:
                    if len(links) > 0:
                        self.linkQ.extend(links)
                        lcount += len(links)
                        #self.pgCount += 1
                
                data = self.htmlparser.get_data()
                if len(data) > 1:
                    self.write_data(url[0], data)
                    self.htmlparser.flush_data()
                    self.pgCount += 1
        print("Crawling Done...")
    
    def write_data(self, url, data):
        with open("data/"+str(time.time()), 'a', encoding='utf-8') as file:
            file.write(url+'\n')
            file.write('\n'.join(data))
    
    def crawl_allowed(self, url):
        global domainRules
        # get root path
        pr = urlparse(url)
        # if domain is not uic.edu, then don't crawl
        if 'uic.edu' not in pr.netloc:
            return False
        # get rules
        rules = domainRules.get(pr.netloc, None)
        # if robots already scanned, then check if current url is allowed
        if rules == False:
            return rules
        elif rules:
            return rules.can_fetch(self.name, url)
        else:
            # read robots and add a rule entry in domainRules
            robotLink = pr.scheme + "://" + pr.netloc + '/robots.txt'
            #print("Robot Link------", robotLink)
            rp = robotparser.RobotFileParser(robotLink)
            try:
                rp.read()
                domainRules[pr.netloc] = rp
                return rp.can_fetch(self.name, url)
            except (TimeoutError, URLError, SSLError, CertificateError):
                domainRules[pr.netloc] = False
                return False