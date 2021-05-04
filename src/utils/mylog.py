import os
import logging
import inspect
from datetime import datetime

class Log:
    

    

    def __init__(self):
        self.formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        self.rootApp = os.getcwd()

    def init(self,profil):
        today = datetime.now()
        dnow = today.strftime(r"%y%m%d") 
        logFilename = "{0}{1}log{1}{3}{2}.log".format(self.rootApp,os.path.sep,profil, dnow)
        errlogFilename = "{0}{1}log{1}{3}err-{2}.log".format(self.rootApp,os.path.sep,profil, dnow) 
        self.intlg = self.setup_logger("genlog", logFilename)            
        self.interrlg = self.setup_logger("errlog", errlogFilename, logging.ERROR)

    
    def setup_logger(self,name, log_file, level=logging.INFO):
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    
    
    def lg(self,mess):       
        print(mess) 
        self.intlg.info(mess)


    def errlg(self,mess):   
        print(mess)      
        mess ="{0!s} \n {1!s}".format(mess, inspect.stack())
        self.intlg.info(mess)
        self.interrlg.error(mess)


