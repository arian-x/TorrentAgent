__author__ = 'arian'
from BeautifulSoup import BeautifulSoup
import requests

class Scrape:
    def __init__(self,link):
        #res = requests.get(link,verify=False)
        self.scrape(link)
    def scrape(self,link):
        res = requests.get(link,verify=False)
        content = res.content
        #self.name_elems = self.driver.find_elements_by_class_name("cellMainLink")
        #self.magnet_elems = self.driver.find_elements_by_class_name("imagnet")
        soup = BeautifulSoup(content)
        self.name_elems = soup.findAll('a',{'class':"cellMainLink"})
        self.magnet_elems = soup.findAll('a',{'class':"imagnet icon16"})
        print len(self.name_elems)
        print len(self.magnet_elems)
        names = []
        for i in self.name_elems:
            name =""
            for j in i.contents:
                name = name + ' ' + j.string
            names.append(name)
       # print names
        magnets = [i.get("href") for i in self.magnet_elems]
       # print magnets
        self.name_mag_dict = {}
        for index,i in enumerate(names):
            self.name_mag_dict[i] = magnets[index]
        print self.name_mag_dict


scp = Scrape("https://kickass.so/search/archer")

