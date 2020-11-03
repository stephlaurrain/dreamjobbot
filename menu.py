import os
import sys
from datetime import datetime

class Menuitem:  
    def __init__(self, command, label, nbparams, jsonfile, isscreen,ret):  
        self.command = command
        self.label = label 
        self.nbparams = nbparams
        self.jsonfile = jsonfile
        self.isscreen =isscreen
        self.ret =ret
  
rootApp = os.getcwd()

def dotail(profil):       
    
    logFilename = "{0}{1}log{1}{3}{2}.log".format(rootApp,os.path.sep,profil, dnow)
    os.system ("tail -f {0}".format(logFilename))

def kill():
    #kill them
    try:
        os.system ("killall /usr/lib/chromium-browser/chromium-browser")
        os.system ("killall /home/pi/dreamjobbot/assets/chromedriver/chromedriver")
    except:
        pass


hardgreen="\033[32m\033[1m"
normalgreen="\033[32m\033[2m"
normalcolor="\033[0m"

def mencol(nb,fonc,comment):
    return "{0}{3} - {4} {1} - {5}{2}".format(hardgreen,normalgreen,normalcolor,nb,fonc,comment) 

def drkcol(str):    
    return "{0}{2}{1}".format(hardgreen,normalcolor,str)           

nbargs = len(sys.argv)
jsonfilefromarg = "default" if (nbargs == 1) else sys.argv[1]


clear = lambda : os.system('clear')
clear()
while True:
    
    print(drkcol("\n\nHi Neo, I'm the DreamJobBot"))
    print(drkcol("I'm ready to farm jobs"))
    print(drkcol("Your wish is my order\n\n"))
    print(drkcol("What I can do for you :\n\n"))

    menulist = []
    menulist.append(Menuitem("doreport","do html report (see json file)",0,jsonfilefromarg,True,False))        
    menulist.append(Menuitem("test", "do test",0,jsonfilefromarg,False,False))     

    for idx,menuitem in enumerate(menulist): 
        print (mencol(idx,menuitem.command,menuitem.label))
        if menuitem.ret:print(drkcol("#####"))

    print (drkcol("#####"))
    print (mencol("55","tail","actual default log"))    
    print (mencol("95","screen -r","access to screen"))
    print (mencol("96","crontab","edit crontab"))
    print (mencol("97","kill","kill processes"))
    print (mencol("98","stop","stop current process"))
    print (mencol("99","exit","exit this menu"))
    dothat = input (drkcol("\n\nReady to farm : "))
    
    today = datetime.now()
    dnow = today.strftime(r"%y%m%d") 
    
    if dothat =="55":
        print(drkcol("\ntail -f default\n"))         
        dotail("default")
    if dothat =="95":
        print(drkcol("\nscreen -r\n"))         
        os.system ("screen -r")   
    if dothat =="96":
        print(drkcol("\nedit crontab\n"))         
        os.system ("crontab -e")   
    if dothat =="97":        
        print(drkcol("\nkill all\n"))         
        kill()
    if dothat =="98":
        print(drkcol("\nstop current process if exists\n"))
        os.system ("touch stop")
    if dothat == "99":
        print(drkcol("\nsee you soon, Neo\n"))
        quit()
    try:
        if int(dothat)<50:
            cmdstr="nop"    
        
            item =menulist[int(dothat)]
            cmd =item.command
            print (cmd)
            prms=int(item.nbparams)
            prmcmdlist=[]
            for i in range(prms):
                prmcmdlist.append(input (drkcol("enter param {0} :".format(i))))
            cmdstr=""
            if item.isscreen:cmdstr="screen "
            cmdstr += "python3 run.py {0} {1}".format(cmd,item.jsonfile)
            for cmdarg in prmcmdlist:
                cmdstr+=" {0}".format(cmdarg)
            print(cmdstr)
            os.system(cmdstr)
        
    except  Exception as e :
        print (e)
        print("\n{0}bad command (open your eyes){1}\n".format(hardgreen,normalcolor))
