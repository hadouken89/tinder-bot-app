from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import os #operation system (for directories and logs)
import re #regex
import logging
import datetime
import random
import re
import prueba01 as pic

#get date time
currentDate = datetime.datetime.now()
date_time = currentDate.strftime("%d-%m-%Y_%H:%M:%S")

#directory to save pic files and logs
current_directory = os.getcwd()

# logging 
FORMAT = '%(asctime)s: %(levelname)s: %(message)s'
log_file = os.path.join(
    current_directory, 'logs/tinder_bot.log')

logging.basicConfig(filename=log_file,
                    format=FORMAT,
                    level=logging.DEBUG)

class WebBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.action = ActionChains(self.driver)
        self.begining = True


    def initWebBot(self):

        self.driver.get("https://tinder.com")    

        #espero a que se habra el popup
        sleep(4)

        btnOptions = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button')
        if( btnOptions.text == 'MORE OPTIONS'):
            btnOptions.click()
            btnFacebook = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button')
        else:
            btnFacebook = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')        
        btnFacebook.click()
  
        base_window = self.driver.window_handles[0]
        popup_window = self.driver.window_handles[1]

        #switch to facebook login popup
        self.driver.switch_to_window(popup_window)

        WebBot.loginFacebook(self)

        sleep(5)
        #switch to main window
        self.driver.switch_to_window(base_window)

        try:
            WebBot.allowTinderPermissions(self)
        except :
            self.driver.implicitly_wait(3)
            WebBot.allowTinderPermissions(self)        

    def loginFacebook(self):
        edtEmail = self.driver.find_element_by_xpath('//*[@id="email"]')
        edtEmail.click()
        edtEmail.send_keys("aca va mi mail")

        edtPassword = self.driver.find_element_by_id("pass")
        edtPassword.click()
        edtPassword.send_keys("aca va mi password")

        btnLoginFacebook = self.driver.find_element_by_id("loginbutton")
        btnLoginFacebook.click()

    def allowTinderPermissions(self):
        btnAllow = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        btnAllow.click()

        btnEnabled = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        btnEnabled.click()

    def autoSwipe(self):
        count = 0
        max_num_swipes = 5
        while count < max_num_swipes:
            self.driver.implicitly_wait(3)
            try:
                self.download_pictures()

                sleep(3)
                self.like()
                count = count + 1
            except Exception:
                try:
                    self.closePopups()
                except:
                    self.like()
                    logging.error("ERROR esta mambeado el tiempo de sincronizacion, espera un ratito...")
                    sleep(6)
                

    def like(self):
        btnLike = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        btnLike.click()

  
    def dislike(self):
        btndislike = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        btndislike.click()

    def closePopups(self):
        try:
            self.keepSwiping()
        except Exception:
            self.closePopupAddHomeScreen()

    def rewind(self):
        btnRewind = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[1]/button')
        btnRewind.click()

    def openProfile(self):
        prof = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div')
        prof.click()   

    def swipePhoto(self):
        btnSwipePhoto = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/svg[2]')
        btnSwipePhoto.click()     

    def keepSwiping(self):
        sleep(2)
        btnKeepSwiping = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        btnKeepSwiping.click()

    def closePopupAddHomeScreen(self):
        btnPopup = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        btnPopup.click()
     

    def openNewTinderTab(self):
        body = self.driver.find_element_by_tag_name('body')
        body.send_keys(Keys.CONTROL + 't')

    def download_pictures(self):
        sleep(2)
        pics = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]')
        num_pics = len(pics.find_elements_by_xpath("./button"))
        next_pic = 1 
        try:
            for x in range(num_pics):
                sleep(2)
                pic_num = x + 1  
                xpath_pic = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[{}]/div/div'.format(pic_num)    
                picture_container = self.driver.find_element_by_xpath(xpath_pic)
                url_picture_no_format = picture_container.value_of_css_property("background-image")

                try:
                    picture_url = self.get_picture_url(url_picture_no_format)
                    utils = pic.DownloadPictures()
                    utils.download_pics(picture_url)
                    # pause to load dom
                    print(" FOTO : {} de {} picture_url".format(pic_num, num_pics))
                    sleep(0.3*random.uniform(1, 1.75))
                    #logging.info(picture_url)
                except Exception:
                        logging.error("ERROR Download pic")
                        print("ERROR al bajar la foto " + Exception)
                
  
                #location = pics.location
                   
                if next_pic < num_pics:
                    next_pic = next_pic + 1 
                    pic_number = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/button[{}]' .format(next_pic)) 
               #     self.action.move_to_element(pic_number).click().perform()
                    pic_number.click()

        except BaseException:
            #  date_time = currentDate.strftime("%d-%m-%Y_%H-%M-%S")
            logging.exception('Failed to get any pictures ' +BaseException )

    def get_picture_url(self, url_pic_no_format):
        regex_url = "(url\(\")(.*)(\"\))"
        m = re.match(regex_url, url_pic_no_format)
        return m.group(2)

    def get_image_path(self):
        body = self.driver.find_element_by_xpath('//*[@id="Tinder"]/body')
        bodyHTML = body.get_attribute('innerHTML')
        startMarker = '<div class="Bdrs(8px) Bgz(cv) Bgp(c) StretchedBox" style="background-image: url(&quot;'
        endMarker = '&'

        if not self.begining:
            urlStart = bodyHTML.rfind(startMarker)
            urlStart = bodyHTML[:urlStart].rfind(startMarker)+len(startMarker)
        else:
            urlStart = bodyHTML.rfind(startMarker)+len(startMarker)

        self.begining = False
        urlEnd = bodyHTML.find(endMarker, urlStart)
        return bodyHTML[urlStart:urlEnd]

### start script ###
logging.info('starting tinder_bot...')
bot = WebBot()
try:
    
    bot.initWebBot()
    try:
        bot.autoSwipe()
    except Exception:
        sleep(3)
        logging.error('ERROR en el autoSwipe')


except BaseException:
    logging.exception('tinder_bot has run into an issue...')



#bot = WebBot()
#bot.openNewTinderTab()

#bot.initWebBot()        
#bot.chat()