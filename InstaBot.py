from timefucntions import time_difference, military_time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import sys
from win32api import GetFileVersionInfo
import random
import argparse
from datetime import datetime

class InstaBot:

  base_url = 'https://www.instagram.com'
  
  def __init__(self,credentials,hashtags,schedule):
    """
    Initializes an instance of InstagramBot Class. 
    
    Calls login method to login into IG

    Args:
      username: str: The Instagram username for a user
      password: str: The Instagram password for a user

    Attributes:
      browser: Selenium.webdriver.Chrome: Chromedriver that is used to automate browser
    """
    self.browser = webdriver.Chrome('chromedriver.exe')
    valid_driver_version = self.check_driver()

    if(valid_driver_version):
      self.credentials = credentials
      self.hashtags = hashtags
      self.schedule = schedule

  def execute(self):
    """Full Marketing Automation Process"""

    self.login()
    self.like_feed()
    for hashtag in self.hashtags:
      self.like_recent_posts(hashtag)
    self.close_browser()

  def check_driver(self):
    """Ensure that chrome and driver are compatible"""

    chrome_version = self.browser.capabilities['browserVersion']
    driver_version = self.browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    chrome_version = chrome_version.split('.')[0]
    driver_version = driver_version.split('.')[0]

    if(chrome_version==driver_version):
      return True
    

  def login(self):
    """Logs into Instagram using user credentials provided"""

    #send credentials to instagram login form
    self.browser.get('{}/accounts/login/'.format(self.base_url))
    time.sleep(random.randint(2,3)) #few seconds for page to load fully
    self.browser.find_element_by_xpath("//input[@name=\"username\"]")\
      .send_keys(self.credentials['username'])
    self.browser.find_element_by_xpath("//input[@name=\"password\"]")\
      .send_keys(self.credentials['password'])
    self.browser.find_element_by_xpath('//button[@type="submit"]')\
      .click()
    time.sleep(4)

    #attempt login 
    try:
      self.browser.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
      .click()
      time.sleep(random.randint(4,5))
    except:
      print("invalid instagram credentials!!!")
      sys.exit()
  
  def like_feed(self):
    """Like the last n posts on feed that are unliked"""
    pass

  def like_recent_posts(self, hashtag):
    """
    Likes recent posts for a given hashtag if post has been posted since
    program run.

    Args:
      hashtag: str: hashtag from hashtags parsed from config file
    """
    self.browser.get(f'{self.base_url}/explore/tags/{hashtag}/')
    time.sleep(2)

    #list of hyperlinks of posts on a page
    links = self.browser.find_elements_by_tag_name('a')
    links = [link.get_attribute('href') for link in links if '.com/p' in link.get_attribute('href')]

    max_likes = random.randint(4,7) 
    like_count = 0

    valid_interval = self.time_since_last_run()

    #loop runs till you have hit the max amount of likes
    for i in range(9,len(links)):
      if(like_count<max_likes):
        self.browser.get(links[i])
        time.sleep(random.randint(1,2))
        self.scroll()
        time.sleep(1)
        
        #only like posts uploaded since last run. ig recent posts not in chronological all the time so cannot simply break out of loop once condition not met
        if(self.time_since_post() <= valid_interval):        
          self.like_post()
          like_count+=1
        
        self.browser.back()
        self.scroll(random.randint(700,1000))
        time.sleep(1)
        self.scroll(random.randint(400,550))
        time.sleep(random.randint(16,25))
      else:
        break

  def time_since_post(self):
    """Return the number of minutes elapsed since the post was uploaded by user to Instagram"""

    date_format = '%Y-%m-%d %H:%M:%S'
    time_tag = self.browser.find_element_by_xpath('//time[@class="_1o9PC Nzb55"]')
    
    #remove the 000Z and replace the T (ISO) b/w date and time
    post_date = time_tag.get_attribute('datetime')[:-5].replace("T", " ")

    post_date = datetime.strptime(post_date, date_format)
    current_date = datetime.strftime(datetime.now(), date_format)
    current_date = datetime.strptime(current_date, date_format)

    time_elapsed = current_date - post_date

    #6 hours buffer due to how instagram stores datetime object
    minutes_elapsed = int((time_elapsed.total_seconds()+(6*3600))/60.0)

    return minutes_elapsed

  def time_since_last_run(self):
    """Return number of minutes elapsed since last run of program"""

    if(len(self.schedule[0].split(':'))==2):
      format = '%I:%M %p'
    else:
      format = '%I:%M:%S %p'

    current_time = datetime.now().strftime(format)
  
    #current time and scheduled time (pick the one with closest gap)  
    diff = [abs(time_difference(current_time, time)) for time in self.schedule]

    min_index = diff.index(min(diff))
    
    current_run = self.schedule[min_index]
    previous_run = self.schedule[min_index-1]

    return time_difference(previous_run, current_run)

    
  def like_post(self):
    """Like an unliked Instagram Post"""

    try:
      self.browser.find_element_by_xpath('//span[@class="glyphsSpriteHeart__outline__24__grey_9 u-__7"]')\
        .click()
    except:
      pass #cannot find span element with unliked class (gray)
    time.sleep(random.randint(2,5))

  def scroll(self, height="document.body.scrollHeight"):
    """imitate a page scoll to the given body height"""

    self.browser.execute_script(f"window.scrollTo(0,{height});")

  def close_browser(self):
    """close our browser session once we are done"""

    self.browser.close()
