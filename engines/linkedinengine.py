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

        def getads(self,site,exclude, doinclude, include):
                self.mainclass.trace(inspect.stack()[0])          
                try:
                        nbads =site["ads"]
                        cptadded=0
                        mainlist = self.mainclass.driver.find_elements_by_class_name("result-card")
                        
                        for res in mainlist:
                                orgurlel = res.find_element_by_css_selector("a")
                                orgurl = orgurlel.get_attribute("href")
                                
                                self.mainclass.waithuman() #voir
                                orgurlel.click()
                                self.mainclass.waithuman()
                                wait = WebDriverWait(self.mainclass.driver, 15)
                                wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "results__detail-view")))
                                adel = self.mainclass.driver.find_element_by_class_name("results__detail-view")
                                adcontain= adel.get_attribute("innerHTML")                        
                                adcontainstriped = self.mainclass.strutils.strip_accents(adcontain.lower()).replace(" ","").replace("'","").replace("&#039","")
                                doit=True
                                for exclwd in exclude:
                                        doit = not (exclwd in adcontainstriped)                                                
                                        if not doit: 
                                                print("FOUND banned word={0}".format(exclwd))
                                                break
                                if doinclude and doit:
                                        for inclwd in include:
                                                doit = inclwd in adcontainstriped                                                
                                                if doit:
                                                        print("==FOUND=={0}".format(inclwd))
                                                        self.report+=self.mainclass.htmlfactory.getfound("==FOUND=={0}".format(inclwd))
                                                        break         
                                if doit:
                                        self.report+=self.mainclass.htmlfactory.geturltolink(orgurl)                                
                                        self.report+=adcontain
                                        cptadded+=1
                                print("cptadded={0}, nbads={1}".format(cptadded,nbads))
                                if cptadded==nbads:break
 #                              self.mainclass.waithuman()
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        def getreport(self, site, distance, location, exclude, doinclude, include, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                    self.dosearch(site, distance, location, words)                      
                    self.getads(site,exclude, doinclude, include)                                   
                    return self.report                    
                except Exception as e:
                        return "{0} {1}".format(e, inspect.stack()[0])
           
           


              
               
    

        
                

        

