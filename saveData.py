import re
import shutil
import wget
import os
from PIL import Image

current_directory = os.getcwd()
webp_dir = os.path.join(
    current_directory, 'webp-pics')

class DownloadPictures():

    def get_picture_url(self, url):
        regex_url = r"(url\(\")(.*)(\"\))"
        m = re.match(regex_url, url)
        return m.group(2)

    def download_pics(self,url_pic):
        try:
           # url = self.get_picture_url(url_pic)
            wget.download(url_pic, webp_dir)

        except Exception :
            print('ERROR Downloading pic')
    

#---------------------
#test = DownloadPictures()
#url_pic = 'url("https://images-ssl.gotinder.com/5e40398ce30e280100c65cc3/640x800_75_843babb8-00d6-44e7-afe6-eea5f89e1ce5.webp")'
#test.download_pics(url_pic)
#-----------------------


