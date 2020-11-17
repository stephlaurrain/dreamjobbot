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


class Glassdoorengine:
      
        def __init__(self, mainclass):                
                self.visitedthissession = list()
                self.dumbthissession = list()
                self.mainclass=mainclass                
                self.report=""                

        def dosearch(self, site, distance, location, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        # 50 : pas de radius
                        # 100 : radius=62, 30 : radius=19                        
                        #dijon-chef-de-projet-informatique-emplois-SRCH_IL.0,5_IC3069836_KO6,33.htm?fromAge=7
                        #PARIS =SRCH_IL.0,5_IC2881970_KO6,33
                        prms="{0}-{1}-emplois-SRCH_IL.0,5_IC{2}_KO6,33.htm?fromAge=7".format(site["geosite"],words.replace(" ","-"), format(location["code"]))
                        radius=""
                        if site["location"]!=50:
                                radius="&radius={0}".format(site["location"])
                        fullurl = "{0}/{1}{2}".format(site["url"],prms,radius)
                        self.mainclass.driver.get(fullurl)
                        
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

    
        
        def treatads(self,res,site,exclude, doinclude, include, nbads):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        orgurlel = res.find_element_by_css_selector("a")
                        orgurl = orgurlel.get_attribute("href")
                        print(orgurl)
                        sitefromlabel=self.getsitefromlabel(res)
                        print(self.mainclass.htmlfactory.getsite(sitefromlabel))
                        self.report+=self.mainclass.htmlfactory.getsite(sitefromlabel)                                
                        self.mainclass.waithuman(1,1)                                
                        self.mainclass.selenutils.doclick(orgurlel)
                        self.mainclass.waithuman(1,1) #voir
                        adel = self.mainclass.driver.find_element_by_id("detailOffreVolet")
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
                                
                        #print("cptadded={0}, nbads={1}".format(cptadded,nbads))
                        
                        btnclose = self.mainclass.driver.find_element_by_css_selector("#PopinDetails > div > div > div > div.modal-header > div > button")
                        self.mainclass.selenutils.doclick(btnclose)
                        
                        
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
                        mainlist = self.mainclass.driver.find_elements_by_class_name("result")
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

        def getreport(self, site, distance, location, exclude, doinclude, include, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                    self.dosearch(site, distance, location, words)  
                    self.getads(site,exclude, doinclude, include)              
                                       
                except Exception as e:
                        mess ="{1!s}{0!s} \n {2!s}".format(e, inspect.stack()[0],inspect.stack())
                        self.report+=self.mainclass.htmlfactory.geterror(mess) 
                return self.report  


              
               
    

        
                

        

