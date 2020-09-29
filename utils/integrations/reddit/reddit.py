import praw
import os
from dotenv import load_dotenv
load_dotenv()

redditClientId = os.environ.get("REDDIT_CLIENT_ID")
redditClientSecret = os.environ.get("REDDIT_CLIENT_SECRET")

class Reddit:
  def __init__(self, userId, userPassword):
    self.userId = userId
    self.userPassword = userPassword
    self.client = praw.Reddit(client_id=redditClientId, client_secret=redditClientSecret, password=self.userPassword, user_agent=self.userId, username=self.userId)

  def postSubReddit(self, redditThread, message):
    try:
      obj = self.client.subreddit("AmongUs").submit(message, url="https://fb.com")
      return {"success": True, "submissionId": obj.id}
      return redditClientSecret
    except Exception as err:
      return {"success": False, "message": str(err)}