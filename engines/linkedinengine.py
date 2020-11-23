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
import math
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


        def dosearch(self, site, location, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        # prms="keywords={0}&location={1}&geoId=&redirect=false&position=1&pageNum=0&f_TP=1,2&distance={2}".format(words, location["geosite"], distance)
                        #attention linkedin : 80km = distance 50, 120km=75 (osef pour le moment)
                        #la distance est en miles
                        dist = location["distance"]*1.6
                        dist = int(math.ceil(dist / 10.0)) * 10
                        prms="f_TPR=r604800&geoId={0}&keywords={1}&location={2}&distance={3}&f_TP=1%2C2&redirect=false&position=1&pageNum=0".format(location["code"],words,location["geosite"],dist)
                        
                        fullurl = "{0}?{1}".format(site["url"],prms)
                        self.mainclass.driver.get(fullurl)                        
                        # f_TP=1%2C2 = la semaine dernière
                        # tri par date sortBy=DD
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise
        

        

        def treatads(self,res,site,exclude, doinclude, include, nbads):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        orgurlel = res.find_element_by_css_selector("a")
                        orgurl = orgurlel.get_attribute("href")
                                
                        self.mainclass.waithuman(15) #voir
                        wait = WebDriverWait(res, 15)
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a")))         
                        self.mainclass.selenutils.doclick(orgurlel)
                        #orgurlel.click()
                        #action = webdriver.common.action_chains.ActionChains(self.mainclass.driver)
                        #action.click(on_element=orgurlel)
                        self.mainclass.waithuman()
                        #wait = WebDriverWait(self.mainclass.driver, 15)
                        #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "results__detail-view")))
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
                        
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        self.report+=self.mainclass.htmlfactory.geterror(str(e)) 
                        #raise
        
                       
        def getads(self,site,exclude, doinclude, include):
                self.mainclass.trace(inspect.stack()[0])          
                try:
                        nbads =site["ads"]
                        cptadded=0
                        mainlist = self.mainclass.driver.find_elements_by_class_name("result-card")
                        
                        for res in mainlist:
                                if self.treatads(res,site,exclude, doinclude, include, nbads):
                                        cptadded+=1
                                if cptadded==nbads:break
                                self.mainclass.waithuman()
                        #print("cptadded={0}, nbads={1}".format(cptadded,nbads))                                
                                        
                except Exception as e:
                        self.mainclass.log.errlg(e)                        
                        raise

        def getreport(self,reportmode,  site, location, exclude, doinclude, include, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                        self.dosearch(site,location, words)   
                        if not self.mainclass.linkedincookclicked:
                                try:                                        
                                        #cssprout= "#artdeco-global-alert-container > div.artdeco-global-alert.artdeco-global-alert--NOTICE.artdeco-global-alert--COOKIE_CONSENT > section > div > div.artdeco-global-alert-action__wrapper > button:nth-child(2)"
                                        cookbutel = self.mainclass.driver.find_element_by_xpath('//div[@id="artdeco-global-alert-container"]/div[1]/section/div/div[2]/button[2]')
                                        self.mainclass.selenutils.doclick(cookbutel)
                                except Exception as e:
                                        print(e)
                                        #pass
                                           
                        if reportmode: 
                                self.getads(site,exclude, doinclude, include)
                        else: input("Waiting for key:\n")                                       
                        
                except Exception as e:
                        mess ="{1!s}{0!s} \n {2!s}".format(e, inspect.stack()[0],inspect.stack())
                        self.report+=self.mainclass.htmlfactory.geterror(mess) 
                return self.report  
           
           


              
               
    

        
                

        

