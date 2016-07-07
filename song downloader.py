import urlparse

__author__ = 'Shashi'
import requests
import re
from bs4 import BeautifulSoup
import urllib2
import os

def SEARCH(QUERY):
    QUERY="index of mp3 "+QUERY
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
    page = requests.get("https://www.google.com/search?q="+QUERY,header)
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    LINKS=[]
    for a in soup.select('.r a'):
        LINKS.append(urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0])
    try:
        return LINKS[:3]
    except:
        return LINKS

def SAVEMP3(url):
    file_name = url.split('/')[-1]
    file_name=file_name.replace('%20',' ')
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print "\r"+status,
    print

    f.close()

def EXTRACT_MP3_LINKS(url):
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
    page = requests.get(url,header)
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    #print type (links)
    for item in links:
        try:
            if ".mp3" in item['href']:
                try:
                    SAVEMP3(item['href'])
                except:
                    pass
                try:
                    SAVEMP3(url+item['href'])
                except:
                    pass
        except:
            pass

def main():
    QUERY=raw_input("ENTER THE SEARCH QUERY: ")
    DOWNLOAD_SITES=SEARCH(QUERY)
    try:
        os.mkdir("SONGS")
    except:
        pass
    try:
        os.mkdir("SONGS/"+QUERY)
    except:
        pass
    os.chdir(("SONGS/"+QUERY))
    for link in DOWNLOAD_SITES:
        try:
            EXTRACT_MP3_LINKS(link)
            print link
        except:
            pass

main()