# CS 582 - Search Engine Project
# Author - Sanjay Ramachandran
# email - sramac22@uic.edu
# UIN - 671035289

from html.parser import HTMLParser
from urllib import parse
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from ssl import SSLError, CertificateError

class NoogleHTMLParser(HTMLParser):
    blacklist = ['script', 'style', 'link', 'meta', 'header', 'svg', 'path', 'nav', 'form', 'input', 'img', 'footer']
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.tag = ''
        self.links = []
        self.baseUrl = ''
    
    def handle_starttag(self, tag, attrs):
        # use below for processing whitelist tag attrs
        #if tag not in blacklist:
        if tag == 'a':
            self.tag = 'nota'
            for (key, value) in attrs:
                if key == 'href':
                    url = parse.urljoin(self.baseUrl, value)
                    self.links.append([url, ''])
                    self.tag = tag
                    break
        else:
            self.tag = tag

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.tag not in NoogleHTMLParser.blacklist:
            #not doing any string translate here. Pre-processor will take care of it.
            data = data.strip()
            if self.tag == 'a':
                self.links[-1][1] = data
            if len(data) > 0:
                self.data.append(data)
    
    def get_links(self, url):
        self.baseUrl = url[0]
        self.links.clear()
        self.flush_data()
        self.tag = ''
        #print("opening--", '-'+url[0]+'-')
        try:
            response = urlopen(url[0])
            if response.status == 200 and 'text/html' in response.getheader('Content-Type'):
                if len(url[1]) > 0:
                    self.data.append(url[1])
                htmlString = response.read().decode('utf-8')
                #print("parsing html....")
                self.tag = ''
                self.feed(htmlString)
                return self.links
        except (HTTPError, TimeoutError, URLError, SSLError, CertificateError, UnicodeDecodeError):
            print("Error - get_links")
        return []
    
    def get_data(self):
        return self.data
    
    def flush_data(self):
        self.data.clear()