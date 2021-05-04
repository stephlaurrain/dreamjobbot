search
          
                        datesel = self.mainclass.driver.find_element_by_css_selector("#triULContainer > li:nth-child(2) > a")
                        #datesel.click()
                        prout = datesel.get_attribute ("href")
                        #print ("prout={0}".format(prout))
                        self.mainclass.driver.get(prout)

                        srchkwzone = self.mainclass.driver.find_element_by_id("idmotsCles-selectized")
                        srchkwzone.send_keys(words)
                        prout = self.mainclass.driver.find_element_by_id("idlieux-selectized")
                        prout.click()
                        btnsrch=self.mainclass.driver.find_element_by_id("btnSubmitRechercheForm")
                        btnsrch.click()

def prout(self):
                scrpt = "$.post('https://candidat.pole-emploi.fr/offres/recherche.rechercheoffre.bloclbb:chargerLBB', {"
                scrpt +='lieux:21231, offresPartenaires: true, rayon:50, tri:0,'
                #.format(self.jsprms.prms["pseudo"], self.jsprms.prms["birthdate_day"], self.jsprms.prms["birthdate_month"],self.jsprms.prms["birthdate_year"])
                scrpt += "motsclefs:'informatique',lieux:21231,rayon:50"
                #scrpt +=" country: '{0}', city: '{1}', member_title: '{3}',zip: {2} ".format(self.jsprms.prms["country"], self.jsprms.prms["city"], self.jsprms.prms["zip"],self.jsprms.prms["member_title"])                     
                scrpt +="} );"
                print (scrpt)
                self.mainclass.driver.execute_script(scrpt)


#prms = "lieux={0}&offresPartenaires=true&rayon={1}&tri=0".format(place["insee"], place["distance"])                    
                    #self.mainclass.driver.get("{0}?{1}".format(site["url"],prms))

                    #print("{0}?{1}".format(site["url"],prms))
                    #print(str(site))



PoleemploiEngine 
       #wait = WebDriverWait(res, 15)
                                #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a")))                                 
                                orgurlel.click()
                                #action = webdriver.common.action_chains.ActionChains(self.mainclass.driver)
                                #action.move_to_element(orgurlel)
                                #action.click()
                                #action.perform()
                                #orgurlel.send_keys("\n") # solution au not clickable
                                #self.mainclass.driver.execute_script("arguments[0].click();", orgurlel)
                                self.mainclass.waithuman(1,1) #voir
                                
                                #wait = WebDriverWait(self.mainclass.driver, 15)
                                #wait.until(EC.presence_of_element_located((By.ID, "detailOffreVolet")))                                        
                                #wait.until(EC.invisibility_of_element_located((By.ID, "loader-container")))
                                adel = self.mainclass.driver.find_element_by_id("detailOffreVolet")
                                #self.mainclass.waithuman() #voir
                                #input ("press key : ")
                                adcontain= adel.get_attribute("innerHTML")                            
                                adcontainstriped = self.mainclass.strutils.strip_accents(adcontain.lower()).replace(" ","").replace("'","").replace("&#039","")
                                doit=True
                                #print("adcontainstriped={0}".format(adcontainstriped))
                                #print("exclude={0}".format(exclude))