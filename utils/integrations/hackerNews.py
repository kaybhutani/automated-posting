# website - https://news.ycombinator.com/news

import requests


class HackerNews:

  def __init__(self):
    self.session = None

  def registerUser(self, userName, userPassword):
    getResponse = self.session.get("https://news.ycombinator.com/submitlink")
    payload = {"creating": "t",
    "switch": "register",
    "acct": userName,
    "pw": userPassword}
    postResponse = self.session.post("https://news.ycombinator.com/submitlink", payload)
    postPageResponse = self.session.get("https://news.ycombinator.com/submitlink")

