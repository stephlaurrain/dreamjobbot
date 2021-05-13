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

        def dosearch(self, site, location, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        #rnge="0-{0}".format(site["ads"]-1)
                        rnge="0-29"
                        prms="lieux={0}&motsCles={1}&offresPartenaires=true&range={2}&rayon={3}&tri=1".format(location["code"], words,rnge,location["distance"] )
                        fullurl = "{0}?{1}".format(site["url"],prms)
                        self.mainclass.driver.get(fullurl)
                        
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

        def getsitefromlabel(self, el):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        originadspanel=el.find_element_by_class_name("media-object")
                        originadimgel =originadspanel.find_element_by_css_selector("img")
                        fromlabel = originadimgel.get_attribute("alt")
                        return fromlabel
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        return "no original site found"
        
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

        def clickcookie(self):
                try:      
                        if not self.mainclass.cookieclicked.apec:                                                          
                                cookbutel = self.mainclass.driver.find_element_by_id("footer_tc_privacy_button_2")                        
                                self.mainclass.selenutils.doclick(cookbutel)
                        self.mainclass.cookieclicked.polemploi = True
                except Exception as e:
                        print(e)
                
        def getreport(self, reportmode, site, location, exclude, doinclude, include, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                      
                        self.dosearch(site, location, words)  
                        self.clickcookie()
                        if reportmode:
                                self.getads(site,exclude, doinclude, include)              
                        else: input("Waiting for key:\n")    
                                       
                except Exception as e:
                        mess ="{1!s}{0!s} \n {2!s}".format(e, inspect.stack()[0],inspect.stack())
                        self.report+=self.mainclass.htmlfactory.geterror(mess) 
                return self.report  


              
               
    

        
                

        

