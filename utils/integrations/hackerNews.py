# website - https://news.ycombinator.com/news
# not in use since they added Captcha verification

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Loading env variables
load_dotenv()

defaultHackernewsId = os.environ.get("HACKERNEWS_LOGIN_ID")
defaultHackernewsPassword = os.environ.get("HACKERNEWS_LOGIN_PASSWORD")
  

class HackerNews:

  def __init__(self):
    self.session = None

  def registerUser(self, userName, userPassword):
    homePageUrl = "https://news.ycombinator.com/submitlink"
    getResponse = self.session.get(homePageUrl)
    payload = {"creating": "t",
    "switch": "register",
    "acct": userName,
    "pw": userPassword}
    postResponse = self.session.post(homePageUrl, payload)
    postPageResponse = self.session.get(homePageUrl)
    soup = BeautifulSoup(postResponse.text)
    opTag = None
    htmlTagRes = soup.find("html")
    
    if htmlTagRes:
      opTag = htmlTagRes.get("op")

    if opTag == 'news':
      return {"success": True}

    return {"success": False}



  def loginUser(self, userName = defaultHackernewsId, userPassword = defaultHackernewsPassword):
    # if session has not been created already
    if self.session == None:
      self.session = requests.Session()

    loginUrl = "https://news.ycombinator.com/login"
    payload = {"goto": "news", "acct": userName, "pw": userPassword}
    loginResponse = self.session.post(loginUrl, payload)
    if loginResponse.text.find("Bad login") > -1:
      print(loginResponse.text)
      return {"success": False}
    return {"success": True}
  
  def getFnid(self):
    submitPageresponse = self.session.get("https://news.ycombinator.com/submit")
    soup = BeautifulSoup(submitPageresponse.text)
    fnidInput = soup.find("input", {"name": "fnid"})
    if fnidInput:
      return fnidInput.get("value")
    return None

  def postProduct(self, title, description, url):
    postProductUrl = "https://news.ycombinator.com/r"
    fnid = self.getFnid()
    payload = {
      "fnid": fnid,
      "fnop": "submit-page",
      "title": title,
      "url": url,
      "text": description
    }
    submitProductResponse = self.session.post(postProductUrl, payload)
    soup = BeautifulSoup(submitProductResponse.text)
    opTag = None
    htmlTagRes = soup.find("html")
    if htmlTagRes:
      opTag = htmlTagRes.get("op")

    if opTag == 'news':
      return {"success": True}
    message = None
    if submitProductResponse.text.find("too fast.") > -1:
      message = "Posting too fast. Slow down."
    else:
      message = submitProductResponse.text
    return {"success": False, "message": message}


if __name__ == "__main__":
    # test
    # hack = HackerNews()
    # res = hack.loginUser()
    # res2 = hack.postProduct("test", "testDesc", "https://fb.com")
    # print(res2)
