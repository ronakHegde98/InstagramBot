from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

class InstaGrowth:
  def __init__(self,username,password):
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
    self.username = username
    self.password = password
    self.page_height = 0
    self.base_url = 'https://www.instagram.com'
    self.login()


  def login(self):

    self.browser.get('{}/accounts/login/'.format(self.base_url))
    time.sleep(5) #few seconds for page to load fully

    email_input = self.browser.find_elements_by_css_selector('form input')[0]
    password_input = self.browser.find_elements_by_css_selector('form input')[1]

    email_input.send_keys(self.username)
    password_input.send_keys(self.password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(5)
  
  def like_feed(self):
    feed_posts = self.browser.find_elements_by_class_name('dCJp8 afkep')
    # like_button = feed_posts.find_elements_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')
    print(len(feed_posts))
    # for i in range(len(feed_posts)):
    #   like_button = feed_posts.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span')
    #   # like_button = feed_posts[i].find_element_by_xpath('/html/body/span/section/main/section/div[2]/div[1]/div/article[{}]/div[2]/section[1]/span[1]/button/span'.format(i+1))
    #   self.browser.execute_script("arguments[0].click();", like_button)#was not clikcing because another element was covering it
    #   print("ronak")
    #   time.sleep(2)

    
  # def trial_scrolls(self):
  #   print(self.browser.execute_script("return document.body.scrollHeight"))
  #   time.sleep(2)
  #   self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
  #   time.sleep(2)
  #   self.browser.execute_script("window.scrollTo(document.body.scrollHeight/2, document.body.scrollHeight);")
  # def follow_user(self, user):
  #   pass

  def close_browser(self):
    self.browser.close()

def get_credentials():
  """      
    reading credentials from credentials.txt
  """
  credentials = {}
  with open('credentials.txt') as f:
    for line in f:
      line=line.strip()
      if("user".upper() in line or "user".lower() in line):
        credentials['username']= line.split(":")[1]
      else:
        credentials['password'] = line.split(":")[1]
  f.close()
  return credentials
  
if __name__ == "__main__":
  credentials = get_credentials()
  bot = InstaGrowth(credentials['username'],credentials['password'])
  # bot.like_feed()