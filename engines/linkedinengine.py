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


class Linkedinengine:
      
        def __init__(self, mainclass):                
                self.visitedthissession = list()
                self.dumbthissession = list()
                self.mainclass=mainclass
                self.report=""                

        def dosearch(self, site, distance, location, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        prms="keywords={0}&location={1}&geoId=&redirect=false&position=1&pageNum=0&f_TP=1,2&distance={2}".format(words, location["geosite"], distance)
                        #attention linkedin : 80km = distance 50, 120km=75 (osef pour le moment)
                        fullurl = "{0}?{1}".format(site["url"],prms)
                        self.mainclass.driver.get(fullurl)                        
                        # f_TP=1%2C2 = la semaine dernière
                        # tri par date sortBy=DD
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        def getads(self,exclude):
                self.mainclass.trace(inspect.stack()[0])          
                try:
                        
                        mainlist = self.mainclass.driver.find_elements_by_class_name("result-card")
                        
                        for res in mainlist:
                                orgurlel = res.find_element_by_css_selector("a")
                                orgurl = orgurlel.get_attribute("href")
                                print(orgurl)
                                orgurlel.click()
                                self.mainclass.waithuman()

                                adel = self.mainclass.driver.find_element_by_class_name("results__detail-view")
                                adcontain= adel.get_attribute("innerHTML")
                                strutl = strutils.Strutils()  
                                adcontainstriped = strutl.strip_accents(adcontain.lower()).replace(" ","").replace("'","").replace("&#039","")
                                doit=True
                                for ex in exclude:
                                        doit = not (ex in adcontainstriped)                                                
                                        if not doit: break
                                if doit:
                                        self.report+=self.mainclass.htmlfactory.geturltolink(orgurl)                                
                                        self.report+=adcontain
 #                              self.mainclass.waithuman()
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        def getreport(self, site, distance, location, exclude, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                    self.dosearch(site, distance, location, words)                      
                    self.getads(exclude)                                  
                    return self.report                    
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise


              
               
    

        
                

        

