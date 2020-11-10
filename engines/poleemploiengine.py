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

        def dosearch(self, site, distance, location, words):
                self.mainclass.trace(inspect.stack()[0])          
                try:                        
                        #rnge="0-{0}".format(site["ads"]-1)
                        rnge="0-29"
                        prms="lieux={0}&motsCles={1}&offresPartenaires=true&range={2}&rayon={3}&tri=1".format(location["code"], words,rnge,distance )
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
        
        def getads(self,site,exclude, doinclude, include):
                self.mainclass.trace(inspect.stack()[0])          
                try:
                        nbads =site["ads"]
                        cptadded=0
                        mainlist = self.mainclass.driver.find_elements_by_class_name("result")
                        for res in mainlist:
                                orgurlel = res.find_element_by_css_selector("a")
                                orgurl = orgurlel.get_attribute("href")
                                print(orgurl)
                                sitefromlabel=self.getsitefromlabel(res)
                                print(self.mainclass.htmlfactory.getsitefrom(sitefromlabel))
                                self.report+=self.mainclass.htmlfactory.getsitefrom(sitefromlabel)
                                #res.click()
                                orgurlel.click()
                                self.mainclass.waithuman()
                                wait = WebDriverWait(self.mainclass.driver, 15)
                                wait.until(EC.invisibility_of_element_located((By.ID, "loader-container")))
                                adel = self.mainclass.driver.find_element_by_id("detailOffreVolet")
                                #input ("press key : ")
                                adcontain= adel.get_attribute("innerHTML")                            
                                adcontainstriped = self.mainclass.strutils.strip_accents(adcontain.lower()).replace(" ","").replace("'","").replace("&#039","")
                                doit=True
                                #print("adcontainstriped={0}".format(adcontainstriped))
                                #print("exclude={0}".format(exclude))
                                for exclwd in exclude:
                                        doit = not (exclwd in adcontainstriped)                                                
                                        if not doit: 
                                                print("FOUND banned word={0}".format(exclwd))
                                                break
                                #print("doit={0}".format(doit))
                                #print("include={0}".format(include))
                                #print("doinclude={0}".format(doinclude))
                                
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
                                btnclose = self.mainclass.driver.find_element_by_css_selector("#PopinDetails > div > div > div > div.modal-header > div > button")
                                btnclose.click()
                                self.mainclass.waithuman()
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
                        self.mainclass.log.errlg(e)
                        raise
       


              
               
    

        
                

        

