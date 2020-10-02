import requests

class Snapmunk:

  def __init__(self):
    self.session = None

  def postProduct(self, userName, userEmail, title, description, yearFounded, website=""):
    firstName = userName
    lastName = ""
    
    # check if lastname is provided and concat middle+last
    nameSplit = userName.split()
    if len(nameSplit) >1:
      firstName = nameSplit[0]
      lastName = " ".join(nameSplit[1:])
    
    payload = {
      "formID": 70171306731144,
      "q3_fullName3[first]": firstName,
      "q3_fullName3[last]": lastName,
      "q6_phoneNumber[area]": "",
      "q6_phoneNumber[phone]": "",
      "q4_email4": userEmail,
      "q7_startupName": title,
      "q8_yearFounded": yearFounded,
      "q9_websiteUrl": website,
      "q12_taglineif": "",
      "q11_description": description,
      "website": website,
      "simple_spc": "70171306731144-70171306731144",
      "embedUrl": "",
      "event_id": "1601640410736_70171306731144_U11aAHZ"
    }

    self.session = requests.Session()
    getResponse = self.session.get("https://www.snapmunk.com/submit-your-startup/")
    postResponse = self.session.post("https://submit.jotform.us/submit/70171306731144/", payload)
    
    # parsing html manually since no json is returned
    if str(postResponse.content).find("Thank You") > -1:
      return {"success": True}
    return {"success": False}