__author__ = 'arian'
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2



class Scrape:
    def __init__(self,link):
        print "sending req"
        res = urllib.urlopen(link)
        print "got the response"
        print res
        soup = BeautifulSoup(res.read())
        names = soup.findAll('a',{'class':'cellMainLink'})
        magnets = soup.findAll('a',{'class':'imagnet icon16 askFeedbackjs'})
        print names
        print magnets






scp = Scrape("https://kickass.so/search/1080p%20category:xxx/")

