import os
import mailslurp_client
import requests
from dotenv import load_dotenv
load_dotenv()

mailSlurpApiKey = os.environ.get("MAILSLURP_API_KEY")

class MailSlurp:

  def __init__(self):
    self.configuration = mailslurp_client.Configuration()
    self.configuration.api_key['x-api-key'] = mailSlurpApiKey
    self.configuration.host = "https://api.mailslurp.com"
    self.client = mailslurp_client.ApiClient(self.configuration)

  def createInbox(self):
    try:
        apiInstance = mailslurp_client.InboxControllerApi(self.client)
        response = apiInstance.create_inbox()
        # https://github.com/mailslurp/mailslurp-client-python/blob/master/docs/Inbox.md
        # return type response
        return {"success": True, "data": response}
    except Exception as err:
        return {"success": False, "message": str(err)}

  def getEmail(self, id):
    # using REST API coz mailSlurp client doesn't support reading mails yet
    header = {
    'x-api-key': mailSlurpApiKey
    }
    res = requests.get('https://api.mailslurp.com/emails/{}'.format(id), headers=header)
    if res.status_code == 200:
      return {"success": True, "email": res.json()}
    return {"success": False, "message": res.json().get('message')}


  def readInbox(self, inboxId):

    apiInstance = mailslurp_client.InboxControllerApi(self.client)
    try:
      emails = apiInstance.get_emails(inboxId)

      return {"success": True, "emails": emails}

    except Exception as err:
      return {"success": False, "message": str(err)}


if __name__ == "__main__":
    inst = MailSlurp()
    inbox= inst.readInbox('c93fc0f7-5a84-43e2-a212-211f0e7fc655') 
    print(inbox.get('emails'))