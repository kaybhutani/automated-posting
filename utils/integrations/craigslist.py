import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

class CraigsList:

  def __init__(self):
    self.session = None
  
  def signUp (self, userEmail):
    try:
      with webdriver.Chrome("/home/kartikay/Desktop/chromedriver") as driver:
      wait = WebDriverWait(driver, 10)
      driver.get("https://accounts.craigslist.org/login?rp=%2Flogin%2Fhome&rt=L")
      import time
      time.sleep(2)
      inp = driver.find_elements_by_name("emailAddress")[0]
      inp.send_keys(userEmail)
      inp.send_keys(Keys.RETURN)
      return {"success": True}
    except Exception as err:
      print(err)
    return {"success": False}

  def readMa
    

