import inspect

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Selenutils(metaclass=Singleton):
    
        def __init__(self, mainclass):
            self.mainclass =mainclass

        def doclickex(self,el):
                self.mainclass.trace(inspect.stack()[0])          
                cpt=0
                while cpt<10:
                        try:         
                                el.click()
                                break
                        except Exception as e:                                
                                print("Ah ben nan y click pô: {0}".format(e))
                                cpt+=1
                                if cpt ==10:raise
                                self.mainclass.waithuman(2)
        
        def doclick(self,el):
                self.mainclass.trace(inspect.stack()[0])          
                try:         
                        el.click()
                except Exception as e:                                
                        print("Ah ben nan y click pô: {0}".format(e))
                        self.mainclass.driver.execute_script("arguments[0].click();", el)
                        self.mainclass.waithuman(2)