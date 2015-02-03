__author__ = 'arian'
#from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Scrape:
    def __init__(self,link):
        self.driver = webdriver.Firefox()
        self.scrape(link)
    def scrape(self,link):
        self.driver.get(link)
        self.name_elems = self.driver.find_elements_by_class_name("cellMainLink")
        self.magnet_elems = self.driver.find_elements_by_class_name("imagnet")
        names = [i.get_attribute('text') for i in self.name_elems]
       # print names
        magnets = [i.get_attribute("href") for i in self.magnet_elems]
       # print magnets
        self.name_mag_dict = {}
        for index,i in enumerate(names):
            self.name_mag_dict[i] = magnets[index]
        print self.name_mag_dict


scp = Scrape("https://kickass.so/alfred-with-license-file-v-2-0-2-t7270011.html")

