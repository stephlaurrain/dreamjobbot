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
import utils.strutils as strutils
import utils.jsonprms as jsonprms
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
                        #pi / docker                
                        if (self.jsprms.prms["raspberry"]):
                                options.add_argument("--no-sandbox")
                                options.add_argument("--disable-dev-shm-usage")
                                options.add_argument("--disable-gpu")
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

        def inithtmlreport(self):  
                self.trace(inspect.stack()[0])
                try:  
                        head="<html>"
                        head+="\n<head>"
                        head+="<link href={0}bootstrap.min.css{0} rel={0}stylesheet{0}>".format(chr(34))
                        head+="<link href={0}dreamjobbot.css{0}rel={0}stylesheet{0}>".format(chr(34))
                        head+="\n</head>"
                        head+="\n<body class={0}main{0}>".format(chr(34))
                        return head
                except Exception as e:
                       self.log.errlg(e) 
                       raise

        def finalizehtmlreport(self):  
                self.trace(inspect.stack()[0])
                try:  
                        end ="</body>"
                        end+="\n</html>"
                        return end
                except Exception as e:
                       self.log.errlg(e) 
                       raise
        
        def doreport(self):  
                self.trace(inspect.stack()[0])
                try:  
                        cptglb=0
                        report = self.inithtmlreport()
                        places = self.jsprms.prms["sites"]
                        for place in places:
                                print(str(place["name"]))

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
                        self.log.lg("=let's crawl=")
                        self.driver = self.init()                        
                        print(command)                                                       
                        if (command=="doreport"):                             
                                
                                self.doreport()
                                
                        
                         
                       

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


              
               
    

        
                

        

