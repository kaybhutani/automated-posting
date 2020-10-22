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
  # res = instance.signUp('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  # print(res)
  res2 = instance.verifyAccount('0c00d0fe-1ce6-44fe-ab7d-9da6da85a8ad@mailslurp.com')
  print(res2)
