import selenium
from selenium import webdriver
from urllib import request
import urllib3
import time
from setuplogger.setup_logger import setup_logger
from inputvalidation.inputvalidation import InputValidation
from pathlib import Path
import os

# seeting up logger



# creating Bing Scraper class
class BingScraper():
    def __init__(self, driver_path, search_query, num_of_images):
        try:
            self.log = setup_logger('bing_scraper', 'bing_scraper.log')
            self.log.info("Initilazition Bing Scrapper")
            self.search_query = search_query
            self.num_of_images = num_of_images
            self.valid = InputValidation(self.search_query, self.num_of_images) # initialize validation class
            self.valid.validate_search_query() # validation of search query
            self.valid.validate_num_of_images() # validation of number of images
            self.driver_path = driver_path
            # self.browser = webdriver.Chrome(driver_path) # initialize chrome driver
            self.timestr = time.strftime("%Y-%m-%d-%H-%M-%S") # get current time
            self.download_folder = str(Path.home() / "Downloads") + "\\" + self.search_query + "-" + self.timestr + "\\"
            if not os.path.exists(self.download_folder):
                os.makedirs(self.download_folder) # creating download folder
            
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            # self.chrome_options.headless = True
            # self.chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            # self.chrome_options.add_argument('-enable-webgl')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.browser = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
            self.log.info("Bing Scrapper Initialized")
            self.filepath = "urls\\" + str(self.search_query) + ".txt"

            if not os.path.isfile(self.filepath):  # check if file exists
                  open(self.filepath, 'w').close() # creating file if not exists
                  self.log.info("Creating file for urls")
        except Exception as e:
            self.log.error("Error in initilazition of Bing Scrapper" + str(e))
            raise e

    def store_links(self):
        """Methode: This methode will store download link in txt file
        Args:
            search_query: search query
            num_of_images: number of images to download
        """
        # start scrapping
        try:
            url = 'http://bing.com/images/search?q=' + self.search_query # main search url
            self.browser.get(url)
            scroll_range = int(self.num_of_images / 100 * 3) + 4 # scroll range is 3 times of number of images
            # start_time = time.time()
            for i in range(scroll_range):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
                try:
                    self.browser.execute_script("document.getElementsByClassName('mm_seemore')[0].click()") # click on see more button
                    self.log.info("Clicked on see more button")
                except selenium.common.exceptions.JavascriptException as e:
                    pass
                time.sleep(3) # wait for page to load
        except Exception as e:
            self.log.error("Error in scrapping" + str(e))
            raise e

        # storing links
        # img_urls = self.browser.find_elements_by_tag_name('img')
        self.log.info("Start finding Xath Webpage")
        img_urls = self.browser.find_elements_by_xpath('//a[@class="iusc"]/div/img') # passing the xpath to find all images
        # filepath = "urls/"+ str(self.search_query) + ".txt"
        f = open(self.filepath, "w+")
        self.log.info("Storing links in file")
        for i in img_urls[:self.num_of_images+10]:
            try:
                img = i.get_attribute('src') # get image url in src tag
                if img is not None and img.startswith('http'):
                    f.write(img + "\n")
                    print(img + "---- Linked Saved") # cooment this line in deployment time
                else:
                    continue # if fails then the next image url will be tried
            except Exception as e:
                self.log.error("Error in storing links" + str(e))
                raise e
        self.log.info("All Links stored in file")
        f.close() # closing the file
        self.browser.close() # closing the browser

    # creating function to download images
    def download_images(self):
        """Methode: This methode will download images
        """
        try:
            self.log.info("Loading URL txt file for DOWNLOADING")
            with open(self.filepath) as f:
                links = [link.rstrip() for link in f] # rstrip removes the new line character from the end of the string
                f.close()
            self.log.info("URL txt file loaded")
        except Exception as e:
            self.log.error("Error in loading URL txt file" + str(e))
        try:
            try:
                self.log.info("Start Downloading images")
                for ix, link in enumerate(links):
                    if ix<=self.num_of_images: # if number of images is less than number of images to download then download
                        self.log.info("Downloading image number: " + str(ix))
                        request.urlretrieve(link, self.download_folder + self.search_query + "_" + str(ix) + ".jpg")
                        print(link + "---- Downloaded")
                self.log.info("Downloading completed")
            except selenium.common.exceptions.InvalidSessionIdException as e:
                pass
            try:
                self.browser.close()
            except selenium.common.exceptions.InvalidSessionIdException as e:
                pass
        except Exception as e:
            self.log.error("Error in downloading images" + str(e))
            raise e
        


    # creating function to check the number of links in file
    def check_links(self):
        """Methode: This methode will check the number of links in file
        """
        try:
            self.log.info("Checking number of Existing links stored in file")
            # filepath = "urls/" + str(self.search_query) + ".txt"
            with open(self.filepath, 'r') as f: # opening the file
                links = [line.rstrip() for line in f] # saving all links in list
                f.close()

            # checking the number of links
            if len(links) >= self.num_of_images:
                self.log.info("Number of links in file is greater than number of images to download")
                # running download function 
                self.download_images()
            else:
                self.log.info("Number of links in file is less than number of images to download")
                os.remove(self.filepath) # removing the file for avoiding duplicate links
                # run store links function here
                self.store_links() # running sotre links function to download the images links in txt file
                time.sleep(2) # wait for 2 seconds
                self.download_images() # running download images function to download the images
        
        except Exception as e:
            self.log.error("Error in checking number of links in file" + str(e))
            raise e

    

                


  
            
        
