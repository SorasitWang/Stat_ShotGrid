# This Python file uses the following encoding: utf-8
from asyncio.windows_events import NULL
from grpc import StatusCode
import requests
import requests
from dotenv import load_dotenv
import os
import json

class Api:
    def __init__(self):
        load_dotenv()
        pass


    ACCESS_TOKEN = None
    scriptName = os.getenv('SCRIPT_NAME')
    scriptKey = os.getenv('API_KEY')
    AUTH_URL = "https://wang.shotgrid.autodesk.com/api/v1/auth/access_token"
    URL = "https://wang.shotgrid.autodesk.com/api/v1"

    def getAccessToken(self):
        payload = {"client_id" : self.scriptName , "client_secret"  : self.scriptKey , "grant_type" : 'client_credentials'}
        #payload = {"username" : "sorasit789@gmail.com" , "password"  : "mek2555137" , "grant_type" : 'password'}
        headers = {'Access-Type': "offline" ,'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        r = requests.post(self.AUTH_URL, data=payload, headers=headers)
        jsonData = json.loads(r.text)
        print(jsonData)
        global ACCESS_TOKEN
        ACCESS_TOKEN = jsonData['access_token']
        print(ACCESS_TOKEN)

    def getTaskEntity(self,taskId):
        url = "{}/entity/Task/{}".format(this.URL,taskId)
        return self.get(url)

    def getAllEntity(self,entity,projectId=None):
        url = "{}/entity/{}".format(self.URL,entity.lower())
        return self.get(url)

    def get(self,url):
        header = header = {"Authorization": "Bearer {}".format(ACCESS_TOKEN), 'Accept': 'application/json'}
        r = requests.get(url,headers=header)
        if (r.status_code == 401):
            print("Token has expired")
            self.getAccessToken()
            self.get(url)
        elif (r.status_code == 200):
            jsonData = json.loads(r.text)
            print(jsonData)
            return jsonData
        else :
            print("Wrong param format")

    #getAccessToken()
   

    '''
    1. get target projectID
    2. find all human_users by relationship
    3. for each user find his task by get following (filter by type&projectID)
    4. for each task find its data ex. duration, status, start-end
    5. visualize that data

     getTaskEntity(3588)




    '''
