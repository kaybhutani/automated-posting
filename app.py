import os
from dotenv import load_dotenv
from utils.integrations.reddit import Reddit
from utils.integrations.apprater import Apprater
from utils.integrations.snapmunk import Snapmunk
from utils.mailSlurp import MailSlurp
from utils.integrations.craigslist import CraigsList

# client = MailSlurp()
# res = client.createInbox()
# print(res)

if __name__ == "__main__":
  instance = CraigsList()
  # res = instance.signUp('9ca0b804-0834-4c6f-a162-bf976231d0de@mailslurp.com')
  # print(res)
  # instance.login()
  instance.post()
