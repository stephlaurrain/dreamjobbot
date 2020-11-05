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
                        report =""
                        mainlist = self.mainclass.driver.find_element_by_class_name("result")
                        mainlist.click()
                        #titleel=self.mainclass.driver.find_element_by_css_selector("#detailOffreVolet > h2")
                        #report+=titleel.get_attribute("innerhtml")
                        adel = self.mainclass.driver.find_element_by_id("detailOffreVolet")
                        report+=adel.get_attribute("innerHTML")
                        print(report)
                        #for eloflist in mainlist:
                        #        eloflist.click()

                        #page_0-19 > li:nth-child(1)
                        return report
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        def getreport(self, site, place, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                    self.mainclass.log.lg("test")
                    self.dosearch(site, place, words)
                    report = self.getads()    
                    return report
                    #return (str(site))
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise
       


              
               
    

        
                

        

