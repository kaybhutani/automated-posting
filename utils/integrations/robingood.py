import requests

class Robingood:

  def __init__(self):
    self.session = None

  def registerUser(self, userEmail, userPassword):
    registerEndpoints = "https://tools.robingood.com/auth/register"
    # application/json
    registerPayload = {"siteId": 389, "email": userEmail, "password": userPassword,
                  "newsletterFrequency": "weekly", "timezone": "Asia/Calcutta"}
    registerResponse = self.session.post(registerEndpoints, json = registerPayload)
    
    if registerResponse.status_code = 200:
      return {"success": True, "data": registerResponse.json}
    return {"success": False}
  
  def loginUser(self, userEmail, userPassword):
    loginEndpoints = "https://tools.robingood.com/auth/login"
    loginPayload = {"siteId": 389,
            "email": userEmail, "password": userPassword}
    loginResponse = self.session.post(loginEndpoints, json = loginEndpoints)

    if loginResponse.status_code = 200:
      return {"success": True, "data": loginResponse.json}
    return {"success": False}

  def registerAndLogin(self, userEmail, userPassword):
    self.session = requests.Session()
    self.session.headers['host'] = "tools.robingood.com"
    self.session.headers['origin'] = 'https://tools.robingood.com'
    homeResponse = self.session.get("https://tools.robingood.com/")
    activityResponse = self.session.get("https://tools.robingood.com/content/activity")
    self.session.get("https://tools.robingood.com/cp/data?siteId=387&orderBy=order&orderType=asc")
    self.session.get("https://tools.robingood.com/content/data?siteId=387&query=ZmM4rtgJE8&categoryId=all&tagId=all&listType=latest&limit=30&offset=0")

    registerResponse = self.registerUser(userEmail, userPassword)
    
    if registerResponse.get("success"):
      loginResponse = self.loginUser(userEmail, userPassword)
      if loginResponse.get("success"):
        return {"success": True}
    
    return {"success": False}