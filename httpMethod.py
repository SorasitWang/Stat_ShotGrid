import requests
import requests
from dotenv import load_dotenv
import os
import json
load_dotenv()
ACCESS_TOKEN = None
scriptName = os.getenv('SCRIPT_NAME')
scriptKey = os.getenv('API_KEY')
AUTH_URL = "https://wang.shotgrid.autodesk.com/api/v1/auth/access_token"
URL = "https://wang.shotgrid.autodesk.com/api/v1"
def getRefreshToken():
    payload = {"client_id" : scriptName , "client_secret"  : scriptKey , "grant_type" : 'client_credentials'}
    headers = {'Access-Type': "offline" ,'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    r = requests.post(AUTH_URL, data=payload, headers=headers)
    jsonData = json.loads(r.text)
    print(jsonData)
    global ACCESS_TOKEN
    ACCESS_TOKEN = jsonData['access_token']
    #return r.text.access_token
def getAccessToken(refreshToken):
    payload = {"refresh_token" : refreshToken ,  "grant_type" : 'refresh_token'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    r = requests.post(AUTH_URL, data=payload, headers=headers)
    print(r.text)
    return r.text


def getTaskEntity(taskId):
    url = "{}/entity/Task/{}".format(URL,taskId)
    print(url)
    print(ACCESS_TOKEN)
    headers = {"Authorization": "Bearer {}".format(ACCESS_TOKEN), 'Accept': 'application/json'}
    r = requests.get(url,headers=headers)
    jsonData = json.loads(r.text)
    print(r.text)
    return r.text
getRefreshToken()
getTaskEntity(3588)