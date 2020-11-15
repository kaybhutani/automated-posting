import praw
import os
from dotenv import load_dotenv
load_dotenv()

redditClientId = os.environ.get("REDDIT_CLIENT_ID")
redditClientSecret = os.environ.get("REDDIT_CLIENT_SECRET")
defaultRedditUserId = os.environ.get("DEFAULT_REDDIT_USER_ID")
defaultRedditUserPassword = os.environ.get("DEFAULT_REDDIT_USER_PASSWORD")

class Reddit:
  def __init__(self, userId = defaultRedditUserId, userPassword = defaultRedditUserPassword):
    self.userId = userId
    self.userPassword = userPassword
    self.client = praw.Reddit(client_id=redditClientId, client_secret=redditClientSecret, password=self.userPassword, user_agent=self.userId, username=self.userId)

  def postSubReddit(self, redditThread, message):
    try:
      obj = self.client.subreddit(redditThread).submit(message)
      return {"success": True, "submissionId": obj.id}
      return redditClientSecret
    except Exception as err:
      return {"success": False, "message": str(err)}