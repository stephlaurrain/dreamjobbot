import inspect

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Htmlfactory(metaclass=Singleton):
    
        def __init__(self, mainclass):
            self.mainclass =mainclass

        def initreport(self):  
                self.mainclass.trace(inspect.stack()[0])
                try:  
                        head="<html>"
                        head+="\n<head>"
                        head+="<link href=/{0}./css/bootstrap.min.css{0} rel={0}stylesheet{0}>".format(chr(34))
                        head+="<link href={0}./css/dreamjobbot.css{0}rel={0}stylesheet{0}>".format(chr(34))
                        head+="\n</head>"
                        head+="\n<body class={0}main{0}>".format(chr(34))
                        return head
                except Exception as e:
                       self.mainclass.log.errlg(e) 
                       raise

        def finalizereport(self):  
                self.mainclass.trace(inspect.stack()[0])
                try:  
                        end ="</body>"
                        end+="\n</html>"
                        return end
                except Exception as e:
                       self.mainclass.log.errlg(e) 
                       raise

        def gettitle(self,title, level):  
                self.mainclass.trace(inspect.stack()[0])
                try:  
                        res="<h{0}>".format(level)
                        res+=title
                        res+="</h{0}>".format(level)
                        return res
                
                except Exception as e:
                       self.mainclass.log.errlg(e) 
                       raise
        
        def getfound(self,mess):  
                self.mainclass.trace(inspect.stack()[0])
                try:  
                        res="<div><span class={0}foundkw{0}>".format(chr(34))
                        res+=mess
                        res+="</span></div>"
                        return res
                
                except Exception as e:
                       self.mainclass.log.errlg(e) 
                       raise
        
        def getsite(self,mess):  
                self.mainclass.trace(inspect.stack()[0])
                try:  
                        res="<div><span class={0}sitefrom{0}>".format(chr(34))
                        res+=mess
                        res+="</span></div>"
                        return res
                
                except Exception as e:
                       self.mainclass.log.errlg(e) 
                       raise

        def geterror(self,mess):  
                self.mainclass.trace(inspect.stack()[0])
                try:  
                        res="<div><span class={0}error{0}>ERROR-".format(chr(34))
                        res+=mess
                        res+="</span></div>"
                        return res
                
                except Exception as e:
                       self.mainclass.log.errlg(e) 
                       raise

        def geturltolink(self,url):
                self.mainclass.trace(inspect.stack()[0])
                try:  
                        res="<div class={0}row jobad{0} ></div>".format(chr(34))
                        res+="<div class={0}col-12 bd-content{0}>".format(chr(34))
                        res+="<span class={0}text-primary{0}>URL : </span><a target={0}blank{0} href={0}{1}{0}>{1}</a>".format(chr(34),url)
                        res+="</div>"
                        return res
                
                except Exception as e:
                       self.mainclass.log.errlg(e) 
                       raise