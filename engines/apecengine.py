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


class Apecengine:
      
        def __init__(self, mainclass):                
                self.visitedthissession = list()
                self.dumbthissession = list()
                self.mainclass=mainclass                
                self.report=""                

        def dosearch(self, site, location, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        prms="lieux={0}&distance={1}&motsCles={2}&anciennetePublication=101851&sortsType=DATE".format(location["code"],location["distance"], words )
                        fullurl = "{0}?{1}".format(site["url"],prms)
                        self.mainclass.driver.get(fullurl)
                        
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        
        def treatads(self,res,site,exclude, doinclude, include, nbads):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        #orgurlel = res.find_element_by_css_selector("a")
                        orgurl = res.get_attribute("href")
                        print(orgurl)
                        self.mainclass.waithuman(1,1) #voir
                        adel = res.find_element_by_class_name("card-offer__header")
                        #input ("press key : ")
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
                        mess ="{1!s}{0!s} \n {2!s}".format(e, inspect.stack()[0],inspect.stack())
                        self.report+=self.mainclass.htmlfactory.geterror(mess) 
                        #raise
        

        def getads(self,site,exclude, doinclude, include):
                self.mainclass.trace(inspect.stack()[0])          
                try:
                        nbads =site["ads"]
                        cptadded=0
                        self.mainclass.waithuman(1,1) #voir
                        maindiv = self.mainclass.driver.find_element_by_class_name("container-result")
                        print ("maindiv={0}".format(maindiv))
                        mainlist = maindiv.find_elements_by_css_selector("a[queryparamshandling='merge']")
                        for res in mainlist:
                                if self.treatads(res,site,exclude, doinclude, include, nbads):
                                        cptadded+=1
                                if cptadded==nbads:break
                                self.mainclass.waithuman(1,1)
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        mess ="{1!s}{0!s} \n {2!s}".format(e, inspect.stack()[0],inspect.stack())
                        self.report+=self.mainclass.htmlfactory.geterror(mess) 
                        #raise

        def getreport(self, site, location, exclude, doinclude, include, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                        self.dosearch(site, location, words)                          
                        if not self.mainclass.apeccookclicked:
                                cookbutel = self.mainclass.driver.find_element_by_class_name("optanon-allow-all")
                                self.mainclass.selenutils.doclick(cookbutel)
                        self.mainclass.apeccookclicked = True
                        self.getads(site,exclude, doinclude, include)              
                
                except Exception as e:
                        mess ="{1!s}{0!s} \n {2!s}".format(e, inspect.stack()[0],inspect.stack())
                        self.report+=self.mainclass.htmlfactory.geterror(mess) 
                return self.report  
       


              
               
    

        
                

        

