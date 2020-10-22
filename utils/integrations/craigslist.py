import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from utils.mailSlurp import MailSlurp
import bs4

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
    
    if verifyUrl != None:
      return {"success": True}
    return {"success": False}








if __name__ == "__main__":
  instance = CraigsList()
  res = instance.signUp('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  print(res)
  res2 = instance.verifyAccount('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  print(res2)

