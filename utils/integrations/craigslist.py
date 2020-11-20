import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from utils.mailSlurp import MailSlurp
import bs4
import time
from dotenv import load_dotenv
import os

# Loading env variables
load_dotenv()

defaultCraigsListId = os.environ.get('CRAIGSLIST_LOGIN_ID')
defaultCraigsListPassword = os.environ.get('CRAIGSLIST_LOGIN_PASSWORD')

chromeDriverPath = "/home/kartikay/Desktop/chromedriver"

class CraigsList:

  def __init__(self):
    self.session = None
    self.driver = webdriver.Chrome(chromeDriverPath)
    wait = WebDriverWait(self.driver, 10)
  
  def signUp (self, userEmail):
    self.userEmail = userEmail
    if userEmail.find('@') != -1:
      userEmail = userEmail.split('@')[0]
    mailSlurpInstance = MailSlurp()
    mailSlurpInstance.emptyInbox(userEmail)
    
    try:
      with webdriver.Chrome(chromeDriverPath) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://accounts.craigslist.org/login?rp=%2Flogin%2Fhome&rt=L")
        time.sleep(2)
        inp = driver.find_elements_by_name("emailAddress")[0]
        inp.send_keys(self.userEmail)
        inp.send_keys(Keys.RETURN)
        return {"success": True}
    except Exception as err:
      print(err)
    return {"success": False}
  
  def parseCraigslistMail(self, emails):
    for email in emails:
      if email.subject.find("New Craigslist Account") != -1:
        return email.id 
    return None

  def getVerifyUrl(self, emailBody):
    soup = bs4.BeautifulSoup(emailBody, "html.parser")
    try:
      return soup.findAll('p')[2].find('a').text
    except Exception as err:
      print(err)
    return None

  def verifyAccount (self, userEmail):
    # convert email to ID 
    if userEmail.find('@') != -1:
      userEmail = userEmail.split('@')[0]

    mailSlurpInstance = MailSlurp()
    readInboxResponse = mailSlurpInstance.readInbox(userEmail)

    if(not readInboxResponse["success"]):
      return {"success": False, "message": "Read inbox failed.\n{}".format(readInboxResponse["message"])}
    emailId = self.parseCraigslistMail(readInboxResponse['emails'])

    if emailId == None:
      return {"success": False, "message": "Read inbox failed."}

    getEmailResponse = mailSlurpInstance.getEmail(emailId)

    if getEmailResponse.get("success") is not True:
      return getEmailResponse
    
    email = getEmailResponse.get("email")
    emailBody = email.get("body")
    verifyUrl = self.getVerifyUrl(emailBody)
    print(verifyUrl)
    if verifyUrl == None:
      return {"success": False, 'message': 'Invalid verify url'}

    try:
      with webdriver.Chrome(chromeDriverPath) as driver:
        wait = WebDriverWait(driver, 10)
        driver.get(verifyUrl)
        time.sleep(2)
        passwordlessBtn = driver.find_element_by_class_name('accountform-btn')[0]
        passwordlessBtn.click()
        return {"success": True}
    except Exception as err:
      print(err)
    return {"success": False}
    
  def login(self, emailId = defaultCraigsListId, password = defaultCraigsListPassword):
    loginUrl = 'https://accounts.craigslist.org/login' 
    self.driver.get(loginUrl)
    time.sleep(2)
    emailInput = self.driver.find_elements_by_name("inputEmailHandle")[0]
    emailInput.send_keys(emailId)
    passwordInput = self.driver.find_elements_by_name("inputPassword")[0]
    passwordInput.send_keys(password)
    passwordInput.send_keys(Keys.RETURN)

  def selectCity(self, city):
    print('City: {}'.format(city))
    try:
      postUrl = 'https://post.craigslist.org/'
      self.driver.get(postUrl)
      time.sleep(2)
      
      # select city part
      selectCityElement = self.driver.find_element_by_class_name('ui-selectmenu-button')
      selectCityElement.click()
      options = self.driver.find_elements_by_class_name('ui-menu-item')
      print(len(options))
      for option in options:
        print(option.text)
        if option.text.find(city) > -1:
          option.click()
          break
      self.driver.find_element_by_name('go').click()
      
      return {'success': True}

    except Exception as error:
      print(error)
    return {'success': False}
  def post(self, postType = 'service offered', postCategory = 'computer services', city='delhi'):
    # cookies = {'name': 'cl_def_hp', 'value': 'delhi'}
    # self.driver.add_cookie(cookies)
    selectCityResponse = self.selectCity(city=city)

    postingTypes = self.driver.find_elements_by_class_name('start-of-grouping')

    for postingType in postingTypes:
      if postingType.text.find(postType) > -1:
        postingType.click()
        break

    categories = self.driver.find_elements_by_class_name('option-label')
    
    for category in categories:
      if category.text.find(postCategory) > -1:
        category.click()
        break

    
    










if __name__ == "__main__":
  instance = CraigsList()
  res = instance.signUp('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  print(res)
  res2 = instance.verifyAccount('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  print(res2)

