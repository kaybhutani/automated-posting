import requests
import datetime

class BetterBusiness:

  def __init__(self):
    self.session = None

  def postProduct(self, productName, address1, address2, stateCode, zipCode, phoneNumber, userEmail, description):
    
    postUrl = 'https://www.bbb.org/api/update/storebusinesslead'
    payload = { "reporterTypeId":"7403",
                "orgName": productName,
                "addressLine1": address1,
                "addressLine2": address2,
                "stateCode": stateCode,
                "postalCode": zipCode,
                "phoneCountryCode": 91,
                "phoneAreaCode": phoneNumber[:3],
                "phoneNumber": phoneNumber[3:],
                "reporterNotes": description,
                "reporterLastName": "",
                "reporterEmail": userEmail,
                "searchedOn": str(datetime.datetime.now()),
                "tobs":[] }
    self.session = requests.Session()
    postResponse = self.session.post(postUrl, payload)
    # Better business API gives no response