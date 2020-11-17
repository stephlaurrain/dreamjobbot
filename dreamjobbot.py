# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime
from time import sleep
import json
import logging
import utils.mylog as mylog
import utils.jsonprms as jsonprms
from utils.strutils import Strutils
from engines.poleemploiengine import Poleemploiengine
from engines.linkedinengine import Linkedinengine
from engines.neuvooengine import Neuvooengine
from engines.monsterengine import Monsterengine
from engines.apecengine import Apecengine
from engines.glassdoorengine import Glassdoorengine
from engines.htmlfactory import Htmlfactory
from engines.selenutils import Selenutils
import inspect
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException


class Bot:
      
        def __init__(self):                
                self.visitedthissession = list()
                self.dumbthissession = list()
                self.htmlfactory = Htmlfactory(self)
                self.selenutils = Selenutils(self)
                self.strutils = Strutils()

        def trace(self,stck):
                #print ("{0} ({1}-{2})".format(stck.function, stck.filename, stck.lineno))
                #print ("{0}".format(stck.function))
                self.log.lg("{0}".format(stck.function))
 

        def waithuman(self,offset=-1, tmp=-1):        
                self.trace(inspect.stack()[0])
                try:                                                
                        loffset = offset
                        loffwait=tmp
                        
                        if (offset == -1):                        
                                loffset = self.jsprms.prms["offsetwait"]
                                loffwait =self.jsprms.prms["wait"]        
                        if (tmp==-1) :
                                loffwait = self.jsprms.prms["defaultwait"]                                
                        random.random()                                
                        res = random.randint(loffset,loffset+loffwait)        
                        self.log.lg("attente de {0} secondes".format(res) )
                        sleep(res)
                
         
                except Exception as e:
                        self.log.errlg(e) 
                        raise
                

        # init
        def init(self):            
                self.trace(inspect.stack()[0])
                try:
                       

                        options = webdriver.ChromeOptions()       
                        if (self.jsprms.prms["headless"]):                                
                                options.add_argument("--headless")
                                options.add_argument("--window-size=1920,1080") # corrige problème not clickable
                        #pi / docker                
                        if (self.jsprms.prms["raspberry"]):
                                options.add_argument("--no-sandbox")
                                options.add_argument("--disable-dev-shm-usage")
                                options.add_argument("--disable-gpu")
                        if self.jsprms.prms["showimages"]:
                                prefs = {"profile.managed_default_content_settings.images": 2}
                                options.add_experimental_option("prefs", prefs)
                        options.add_argument("user-agent={0}".format(self.jsprms.prms["useragent"]))            
                        options.add_argument("--start-maximized")
                        
                        driver = webdriver.Chrome(executable_path=self.chromedriverbinpath, options=options)
                        driver.implicitly_wait(self.jsprms.prms["implicitlywait"])
                        
                        return driver
                except Exception as e:                             
                        self.log.errlg(e)
                        raise



        def stop(self):  
                stopfile ="{0}{1}stop".format(self.rootApp,os.path.sep)                
                res = path.exists(stopfile)
                if (res):                                                
                        self.log.lg("=STOP CRAWLING=")
                return res  

        def removestop(self):  
                stopfile ="{0}{1}stop".format(self.rootApp,os.path.sep)                
                res = path.exists(stopfile)
                if (res):os.remove(stopfile)

        def getlocationfromplace (self,sitename, place):        
                self.trace(inspect.stack()[0])
                try:                                      
                      
                        for location in place["location"]:
                                #print(location["site"])
                                if location["site"]==sitename:
                                        #print("###{0}###".format(location))
                                        return location
                
         
                except Exception as e:
                        self.log.errlg(e) 
                        raise
        
        def doreport(self, reportname):  
                self.trace(inspect.stack()[0])
                try:  
                        
                        report = self.htmlfactory.initreport()
                        places = self.jsprms.prms["places"]
                        keywords = self.jsprms.prms["keywords"]
                        sites = self.jsprms.prms["sites"]
                        doinclude = self.jsprms.prms["doinclude"]
                        exclude = self.jsprms.prms["exclude"]
                        include = self.jsprms.prms["include"]
                        self.apeccookclicked = False
                        for place in places:                                
                                #print(place["name"])
                                for kw in keywords:
                                        #words=kw["words"]
                                        #wordstostr = '+'.join(words)
                                        report+=self.htmlfactory.gettitle(kw,2)
                                        for site in sites:
                                                name=site["name"]
                                                #print(site["name"])
                                                print(self.getlocationfromplace(name,place))                                                
                                                location =self.getlocationfromplace(name,place)
                                                
                                                if name=="poleemploi":
                                                        if site["ison"]:                                                                
                                                                report+=self.htmlfactory.gettitle(site["name"],1)
                                                                poleemploiengine = Poleemploiengine(self)                                                                                  
                                                                report+=poleemploiengine.getreport(site, location, exclude, doinclude, include, kw)
                                                if name=="linkedin":
                                                        if site["ison"]:
                                                                report+=self.htmlfactory.gettitle(site["name"],1)
                                                                linkedinengine = Linkedinengine(self)  
                                                                report+=linkedinengine.getreport(site, location, exclude, doinclude, include, kw)
                                                if name=="neuvoo":
                                                        if site["ison"]:
                                                                report+=self.htmlfactory.gettitle(site["name"],1)                                                                
                                                                neuvooengine = Neuvooengine(self)                                                                                  
                                                                report+=neuvooengine.getreport(site, location, exclude, doinclude, include, kw)                
                                                if name=="monster":
                                                        if site["ison"]:                                         
                                                                report+=self.htmlfactory.gettitle(site["name"],1)                       
                                                                monsterengine = Monsterengine(self)                                                                                  
                                                                report+=monsterengine.getreport(site, location, exclude, doinclude, include, kw)                
                                                if name=="apec":
                                                        if site["ison"]:
                                                                report+=self.htmlfactory.gettitle(site["name"],1)
                                                                apecengine = Apecengine(self)                                                                                  
                                                                report+=apecengine.getreport(site, location, exclude, doinclude, include, kw)     
                                                                
                                                if name=="indeed":
                                                        if site["ison"]:
                                                                pass
                                                if name=="adzuna":
                                                        if site["ison"]:
                                                                pass
                                                if name=="glassdoor":
                                                        if site["ison"]:
                                                                report+=self.htmlfactory.gettitle(site["name"],1)
                                                                glassdoorengine = Glassdoorengine(self)                                                                                  
                                                                report+=glassdoorengine.getreport(site, location, exclude, doinclude, include, kw)     
                                                                
                                                
                        report+=self.htmlfactory.finalizereport()
                        today = datetime.now()
                        dnow = today.strftime(r"%Y%d%m") 
                        reportfn = "{0}{1}data{1}reports{1}{2}{3}.html".format(self.rootApp,os.path.sep,dnow,reportname)  
                        if path.exists(reportfn):os.remove(reportfn)
                        with open(reportfn,"w") as reportfile:
                                reportfile.write(report)

                except Exception as e:
                       self.log.errlg(e) 
                       raise

        def main(self):
                          
                try:
                        self.rootApp = os.getcwd()
                        # InitBot
                        # args
                        self.removestop() #remove stop file
                        nbargs = len(sys.argv)
                        command = "doreport" if (nbargs == 1) else sys.argv[1]
                        #command = "test" if (nbargs == 1) else sys.argv[1]
                        # json parameters from file
                        param = "default" if (nbargs < 3) else sys.argv[2].lower()                        
                        print("params=", command, param)

                        #logs
                        self.log = mylog.Log()
                        self.log.init(param)
                        self.trace(inspect.stack()[0])     
                        jsonFn ="{0}{1}data{1}{2}.json".format(self.rootApp,os.path.sep,param)                        
                        self.jsprms = jsonprms.Prms(jsonFn)                                              
                        self.chromedriverbinpath ="{0}{1}assets{1}chromedriver{1}chromedriver".format(self.rootApp,os.path.sep)
                        self.test = self.jsprms.prms["test"]
                        self.log.lg("=dreamjobbot V1.1346, let's crawl=")
                        self.driver = self.init()                        
                        print(command)                                                       
                        if (command=="doreport"):                             
                                
                                self.doreport(param)
                                #self.waithuman(1500)
                                #input("enter key")
                                self.driver.close()
                                self.driver.quit()
                        if (command=="test"):   
                                print(inspect.stack()[0])

                        self.log.lg("=THE END COMPLETE=")

                except Exception as e:
                        self.log.errlg(e)
                        raise
       
        def testo(self):         
                self.trace(inspect.stack()[0])
                
                try:     
                        
                        pass

                except Exception as e:
                        self.log.errlg(e)  
                        self.driver.close()
                        self.driver.quit()        


              
               
    

        
                

        

