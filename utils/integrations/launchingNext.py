import requests

class LaunchingNext:

  def __init__(self):
    self.session = None

  def getMathAns(self):
    # for now the ans is always 5
    # otherwise need to scrape and get sum
    return "5"
  def postProduct(self, startupName, website, title, description, tags, userName, userEmail ):
    
    self.session = requests.Session()
    submitProductUrl = "https://www.launchingnext.com/submit.php"
    
    tagsString = ""
    for tag in tags:
      tagsString += tag + ","
    tagsString = tagsString[:-1]
  
  mathAns = self.getMathAns()
    payload = {
      "startupname": startupName,
      "startupurl": website,
      "description": title,
      "fulldescription": description,
      "tags": tagsString,
      "funding": 0,
      "boardmembers": 0,
      "user": userName,
      "email": userEmail,
      "math": mathAns,
      "formSubmit": "Submit Startup"
    }
    submitProductResponse = self.session.post(submitProductUrl, payload)
    
    # since there is no check for wrong input on website
    return {"success": True}

