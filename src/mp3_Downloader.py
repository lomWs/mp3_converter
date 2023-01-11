from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager #automatic driver installation
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import os.path
from  threading import Thread

#GLOBAL CONSTANT

YOUTUBE_LINK = "https://www.youtube.com/results?search_query="
CONVERTER_LINK = "https://notube.li/it/youtube-app-v20"


######## DOWNLOADER CLASS ########
class Mp3_Downloader(Thread):#using subclass

    
    #### Costructor #### 
    def __init__(self,user_query,download_path):
        #inizialize the thread
        Thread.__init__(self)
        #inizialize variables and options
        self.user_query = user_query
        
        self.download_path = download_path
        self.song = ""
        options  = self.set_option()
        #automatic driver installation
        chrome_driver = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(service = Service(chrome_driver))
             
        self.driver = webdriver.Chrome(options=options)
        
           
    #### Web driver options setter ####   
    def set_option(self):
        options = Options()
        
        if self.download_path != "":#if user don't specify the path it takes the standard download path
            #change download directory
            prefs = {"download.default_directory" : self.download_path}#'C:\prova' path type
            options.add_experimental_option("prefs", prefs)
        
        #hide windows
        options.add_argument('--headless')
        
        return options
    
    
    #### Get youtube video's link ####
    def yt_link(self):
        #go on "youtube + name of song"
        self.driver.get(YOUTUBE_LINK+self.user_query)
        self.driver.implicitly_wait(10)
        #wait the page and click accept button
        acbutton = WebDriverWait(self.driver , 15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button')))
        acbutton.click()
        self.driver.implicitly_wait(10)
        #save video's link
        link = self.driver.find_element(By.XPATH,'//*[@id="video-title"]').get_attribute('href')
        
        #grab the name of the video
        self.song = self.driver.find_element(By.XPATH,'//*[@id="video-title"]').get_attribute('title')
        
        return link
    
    #### Download the file in mp3 ####
    def download_song(self):  
        
        #get link of the first video
        link = self.yt_link()
        
        #open new tab with js script
        self.driver.execute_script("window.open('');")
        time.sleep(5)
        
        #switch to converter page
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(CONVERTER_LINK)
        
        #wait the page and paste the link
        WebDriverWait(self.driver , 15).until(EC.element_to_be_clickable((By.ID,'keyword'))).send_keys(link)
        WebDriverWait(self.driver , 15).until(EC.element_to_be_clickable((By.ID,'submit-button'))).click()
        
        #start downloading
        WebDriverWait(self.driver , 17).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="downloadButton"]'))).click()
        
        #formatting song name to check the downoload status
        self.song = self.song +".mp3"
        
        #close spam pages
        self.close_up()
        
        #check download_status
        while not self.download_status():   
            time.sleep(1)
        
        #close session
        self.driver.quit()
        
        
    #### Check download status ####
    def download_status(self):#if download is finished close the pages
        if os.path.isfile(self.download_path +"\\" +self.song):
            return True
        else:
            return False
        
    #### Close spam pages ####  
    def close_up(self): #close unless page
        handles = self.driver.window_handles
        handles.remove(handles[1])#removing converter page and close others
        for tab in handles:
            self.driver.switch_to.window(tab)
            
            time.sleep(1)
            self.driver.close()
            
            
    def run(self):#thread's method
        #start download
        self.download_song()
                 
######## /DOWNLOADER CLASS ########


