__author__ = 'arian'
#from BeautifulSoup import BeautifulSoup
#import urllib
#import urllib2
#import cookielib
from urllib.request import urlopen


class Scrape:
    def __init__(self,link):
        #cj = cookielib.CookieJar()
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #opener.add_handler([('User-agent', "Magic Browser")])
        #urllib2.install_opener(opener)

        print("sending req")
        #res = opener.open(link)
#        res = urllib.request.urlopen("https://kickass.so/search/1080p%20category:xxx/")

        html = urlopen("https://kickass.so/").read()
        decoded_str = html.decode("utf8")
        encoded_str = decoded_str.encode("utf8")
        print(encoded_str)
#        print("got the response")
        #print res
        #soup = BeautifulSoup(res.read())
        #names = soup.findAll('a',{'class':'cellMainLink'})
        #magnets = soup.findAll('a',{'class':'imagnet icon16 askFeedbackjs'})
        #print names
        #print magnets






scp = Scrape("https://kickass.so/search/1080p%20category:xxx/")

