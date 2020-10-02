import requests


class Apprater:
  def __init__(self):
    self.session = None
  
  def postProduct(userName, userEmail, title, website, description, tags):
    tagsString = ""
    for tag in tags:
      tagsString+= tag + ","
    tagsString = tagsString[:-1]
    payload = {
      "user-submitted-name": userName,
      "user-submitted-email": userEmail,
      "user-submitted-title": title,
      "user-submitted-url[]": website,
      "user-submitted-content": description,
      "user-submitted-tags": tagsString,
      "user-submitted-image[]": "(binary)",
      "usp-min-images": 0,
      "usp-max-images": 20,
      "redirect-override":"https://apprater.net/promote-your-app/",
      "user-submitted-post": "Submit Product for Review",
      "usp-nonce": "5d638a3908"
    }
    self.session = requests.Session()
    getResponse = self.session.get('https://apprater.net/add/')
    postResponse = self.session.post('https://apprater.net/add/', payload)
    self.session.close()