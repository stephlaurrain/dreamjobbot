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

        def dosearch(self, site, location, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        # 50 : pas de radius
                        # 100 : radius=62, 30 : radius=19                        
                        #dijon-chef-de-projet-informatique-emplois-SRCH_IL.0,5_IC3069836_KO6,33.htm?fromAge=7
                        #PARIS =SRCH_IL.0,5_IC2881970_KO6,33
                        words=words.replace(" ","-")
                        
                        ln = len("{0}-{1}".format(location["geosite"],words))
                        prms="{0}-{1}-emplois-SRCH_IL.0,5_IC{2}_KO6,{3}.htm?fromAge=7".format(location["geosite"],words, location["code"],ln)
                        print(prms)
                        #https://www.glassdoor.fr/Emploi/dijon-chef-de-projet-informatique-emplois-SRCH_IL.0,5_IC3069836_KO6,33.htm
                        radius=""
                        if location["distance"]!=50:
                                radius="&radius={0}".format(location["distance"])
                        fullurl = "{0}/{1}{2}".format(site["url"],prms,radius)
                        print(fullurl)
                        self.mainclass.driver.get(fullurl)
                        #input ("key")
                        
                except Exception as e:
                        self.mainclass.log.errlg(e)
                        raise

    
        
        def treatads(self,res,site,exclude, doinclude, include, nbads):
                self.mainclass.trace(inspect.stack()[0])          
                try:                   
                        #orgdiv =   res.find_element_by_css_selector("div")   
                        #print (res.get_attribute("innerHTML") )
                        #
                        orgurlel = res.find_element_by_class_name("jobLink")
                        orgurl = orgurlel.get_attribute("href")
                        print(orgurl)   
                        #modal_closeIcon
                        self.mainclass.waithuman(1,1)                                
                        self.mainclass.selenutils.doclick(orgurlel)
                        self.mainclass.waithuman(1,1) #voir
                        adel = self.mainclass.driver.find_element_by_id("JDWrapper")                        
                        adcontain= adel.get_attribute("innerHTML")
                        adcontain = adcontain.replace("h1>","h3>")                            
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
                        jlgrid=self.mainclass.driver.find_element_by_class_name("jlGrid")
                        mainlist = jlgrid.find_elements_by_css_selector("li")
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
                        #print ("cookieclicked={0}".format(self.mainclass.cookieclicked.glassdoor))
                        if not self.mainclass.cookieclicked.glassdoor: 
                                cookbutel = self.mainclass.driver.find_element_by_id("onetrust-accept-btn-handler")
                                #print ("cookbutel={0}".format(cookbutel))
                                self.mainclass.selenutils.doclick(cookbutel)
                        self.mainclass.cookieclicked.glassdoor = True
                except Exception as e:
                        print(e)

        def getreport(self, reportmode, site, location, exclude, doinclude, include, words):
                self.mainclass.trace(inspect.stack()[0])         
                try:
                        self.dosearch(site, location, words)  
                        self.clickcookie()
                        
                        #input("prout")
                        if reportmode:
                                self.getads(site,exclude, doinclude, include)       
                        else: input("Waiting for key:\n")           
                                       
                except Exception as e:
                        mess ="{1!s}{0!s} \n {2!s}".format(e, inspect.stack()[0],inspect.stack())
                        self.report+=self.mainclass.htmlfactory.geterror(mess) 
                        print (mess)
                return self.report  


              
               
    

        
                

        

