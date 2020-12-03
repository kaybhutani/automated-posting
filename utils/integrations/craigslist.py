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

clDefaultTypes = {
  'EVENT_OR_CLASS': 'event / class',
  'SERVICE': 'service offered',
  'COMMUNITY': 'community'
}

clDefaultCategories = {
  'SERVICE': ["automotive services", "beauty services", "cell phone / mobile services", "computer services", "creative services", "cycle services", "event services", "farm & garden services", "financial services", "household services", "labor / hauling / moving", "legal services", "lessons & tutoring", "marine services", "pet services", "real estate services", "skilled trade services", "small biz ads", "travel/vacation services", "writing / editing / translation"],
  'COMMUNITY': ["activity partners (please do not post personals on craigslist)", "artists", "childcare", "general community (no politics here please)", "groups", "local news and views (no national or international issues here please)", "lost & found", "missed connections", "musicians", "pets (no animal sales or breeding -- rehoming with…ption fee is ok -- info on free to good home ads)", "politics", "rants & raves", "rideshare", "volunteers"],
  'EVENT_OR_CLASS': ["I'm selling a small number of tickets to an event", "My business is having a sale", "I'm offering an event-related service (rentals, transportation, etc.)", "I'm advertising a garage sale, estate sale, moving sale, flea market, or other non-corporate sale", "I'm advertising a class or training session", "I'm advertising an event, other than the above"]

}


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
    print('Selecting City: {}'.format(city))
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
      return {'success': False, 'message': str(error)}


  def selectPostType(self, postType):
    print('Selecting post type: ', postType)
    try:

      postingTypes = self.driver.find_elements_by_tag_name('li')
      print(len(postingTypes))
      for postingType in postingTypes:
        print(postingType.text)
        if postingType.text.find(postType) > -1:
          postingType.click()
          break
      return {'success': True}
    except Exception as error:
      print(error)
      return {'success': False, 'message': str(error)}

  def selectCategory(self, postCategory):
    print('Selecting post category: ', postCategory)
    try:
      categories = self.driver.find_elements_by_tag_name('label')
        
      for category in categories:
        print(category.text)
        if category.text.find(postCategory) > -1:
          category.click()
          break
      return {'success': True}
    except Exception as error:
      print(error)
      return {'success': False, 'message': str(error)}

  def addPostDetails(self, postTitle, postalCode, city, postDescription):
    try:
      # fetching input elements
      postingTitle = self.driver.find_element_by_name('PostingTitle')
      postingCity = self.driver.find_element_by_name('geographic_area')
      postingPostalCode = self.driver.find_element_by_name('postal')
      postingDescription = self.driver.find_element_by_name('PostingBody')
      
      # send details

      postingTitle.send_keys(postTitle)
      postingCity.send_keys(city)
      postingPostalCode.send_keys(postalCode)
      postingDescription.send_keys(postDescription)

      # submit post data
      self.driver.find_element_by_name('go').click()
      return {'success': True}
    except Exception as error:
      print(error)
      return {'success': False, 'message': str(error)}


  def post(self, postType, postCategory, postTitle = '', postalCode = '', city='delhi', postDescription = ''):
    # cookies = {'name': 'cl_def_hp', 'value': 'delhi'}
    # self.driver.add_cookie(cookies)
    
    # check postType and postCategory

    postType = clDefaultTypes.get(postType)
    
    # validate type and categories
    if not postType:
      print('Invalid Post type')
      return {'success': False, 'message': 'Invalid Post type'}
    
    if postCategory > len(clDefaultCategories.get(postType)):
      print('Invalid Post category')
      return {'success': False, 'message': 'Invalid Post category'}
    
    # category int to string
    postCategory = clDefaultCategories.get(postType)[postCategory]


    selectCityResponse = self.selectCity(city=city)

    # select post type
    postTypeSelectResponse = self.selectPostType(postType)
    print(postTypeSelectResponse)

    # select category
    postCategorySelectResponse = self.selectCategory(postCategory)
    print(postCategorySelectResponse)

    # add post details
    addPostDetailsResponse = self.addPostDetails(postTitle, postalCode, city, postDescription)
    print(addPostDetailsResponse)

    # images part
    # skipping image upload for now
    try:
      imageBtn = self.driver.find_elements_by_name('go')[1]
      
      # submit only if image page is shown
      # prevents clicking Publish button
      if imageBtn.text.find('image') >-1:
        imageBtn.click()
    except Exception as err:
      print('Error when skipping images: ', err)
    
    # publish ad page
    # submit once more to publish
    # self.driver.find_element_by_name('go').click()

    
    










if __name__ == "__main__":
  instance = CraigsList()
  res = instance.signUp('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  print(res)
  res2 = instance.verifyAccount('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  print(res2)

