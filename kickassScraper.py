__author__ = 'arian'
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import cookielib



class Scrape:
    def __init__(self,link):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.add_handler([('User-agent', "Magic Browser")])
        urllib2.install_opener(opener)

        print "sending req"
        res = opener.open(link)
        print "got the response"
        #print res
        soup = BeautifulSoup(res.read())
        names = soup.findAll('a',{'class':'cellMainLink'})
        magnets = soup.findAll('a',{'class':'imagnet icon16 askFeedbackjs'})
        print names
        print magnets






scp = Scrape("https://kickass.so/search/1080p%20category:xxx/")

