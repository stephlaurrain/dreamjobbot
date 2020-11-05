# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime
from time import sleep
import json
import logging
import inspect
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException


class Poleemploiengine:
      
        def __init__(self, mainclass):                
                self.visitedthissession = list()
                self.dumbthissession = list()
                self.mainclass=mainclass
                self.report=""                

        def dosearch(self, site, place, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:
                        rnge="0-{0}".format(site["ads"]-1)
                        prms="lieux={0}&motsCles={1}&offresPartenaires=true&range={2}&rayon={3}&tri=1".format(place["insee"], words,rnge,place["distance"] )
                        fullurl = "{0}?{1}".format(site["url"],prms)
                        self.mainclass.driver.get(fullurl)
                        
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        def getads(self):
                self.mainclass.trace(inspect.stack()[0])          
                try:
                        
                        mainlist = self.mainclass.driver.find_elements_by_class_name("result")
                        for res in mainlist:
                                orgurl = res.find_element_by_css_selector("a").get_attribute("href")
                                print(orgurl)
                                #
                                self.report+=self.mainclass.htmlfactory.geturltolink(orgurl)
                                res.click()
                                self.mainclass.waithuman()
                                wait = WebDriverWait(self.mainclass.driver, 15)
                                wait.until(EC.invisibility_of_element_located((By.ID, "loader-container")))
                                adel = self.mainclass.driver.find_element_by_id("detailOffreVolet")
                                #input ("press key : ")
                                self.report+=adel.get_attribute("innerHTML")                                
                                btnclose = self.mainclass.driver.find_element_by_css_selector("#PopinDetails > div > div > div > div.modal-header > div > button")
                                btnclose.click()
                                self.mainclass.waithuman()
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        def getreport(self, site, place, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                    self.dosearch(site, place, words)  
                    self.getads()              
                    return self.report                    
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise
       


              
               
    

        
                

        

