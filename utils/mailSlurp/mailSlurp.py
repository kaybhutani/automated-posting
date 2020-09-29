import os
import mailslurp_client
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
        response = api_instance.create_inbox()
        return {"success": True, "data": response}
    except Exception as err:
        return {"success": False, "message": str(err)}
