# This Python file uses the following encoding: utf-8
from asyncio.windows_events import NULL
import pprint
import requests
import requests
from dotenv import load_dotenv
import os
import json
import concurrent.futures
import datetime
import numpy as np
from entity.note import Note
from entity.task import Task
from entity.user import User
from entity.project import Project
np.set_printoptions(threshold=1000)


MAXTHREAD = 450
class Api:
    def __init__(self):
        load_dotenv()
        self.ACCESS_TOKEN = None
        self.scriptName = os.getenv('SCRIPT_NAME')
        self.scriptKey = os.getenv('API_KEY')
        self.AUTH_URL = "https://wang.shotgrid.autodesk.com/api/v1/auth/access_token"
        self.URL = "https://wang.shotgrid.autodesk.com/api/v1"
        
    def getAccessToken(self):
        
        payload = {"client_id" : self.scriptName , "client_secret"  : self.scriptKey , "grant_type" : 'client_credentials'}
        headers = {'Access-Type': "offline" ,'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        r = requests.post(self.AUTH_URL, data=payload, headers=headers)
        jsonData = json.loads(r.text)
        self.ACCESS_TOKEN = jsonData['access_token']
        print(self.ACCESS_TOKEN)

    def getTaskData(self,taskId):
        url = "{}/entity/Task/{}".format(self.URL,taskId)
        return self.get(url)

    def getAllEntity(self,entity,projectId=None):
        url = "{}/entity/{}".format(self.URL,entity.lower())
        return self.get(url)

    

    def getAllUser(self,project:Project):
        projectID = project.id
        url = "{}/entity/projects/{}/relationships/users".format(self.URL,projectID)
        res = self.request("GET",[url])[0]
        for user in res[1]['data']:
            #project.users[17] = User(17)
            project.users[user['id']] = User(user['id'])
           
    
    def getUserFollowing(self,project : Project,type=None):
        urls =[]
        for id in project.users.keys():
            #gen url
            urls.append("{}/entity/human_users/{}/following?entity={}&project_id={}"
                .format(self.URL,id,type.lower(),project.id))
        res = self.request("GET",urls)
        for e in res:
            #0 : url , 1 : data
            start = 60
            end = e[0].find("/",start+1)
            userId = int(e[0][start+1:end])
            for entity in e[1]['data']:
                if type == "Task":
                    tmp = Task(entity["id"])
                    project.tasks[entity["id"]] = tmp
                    project.users[userId].tasks[entity["id"]] = tmp
                elif type == "Note":
                    tmp = Note(entity["id"])
                    project.notes[entity["id"]] = tmp
                    project.users[userId].notes[entity["id"]] = tmp
            #temp
            break
        

    def getInfo(self,project:Project,type,info="attributes"):
        if type=="Task":
            urls = [ "{}/entity/{}/{}".format(self.URL,type,id) for id in project.tasks.keys()]
        elif type=="Note" :
            urls = [ "{}/entity/{}/{}".format(self.URL,type,id) for id in project.notes.keys()]
       
        res = self.request("GET",urls)
        c = 0
        for e in res:
            start = len(self.URL)+len("/entity/")+len(type)
            end = e[0].find("/",start+1) if e[0].find("/",start+1)!=-1 else len(e[0])+1
            try :
                c+=1
                id = int(e[0][start+1:end])
                if type=="Task":
                    #Task in User also change
                    project.tasks[id].setValue(e[1]["data"][info])
                elif type=="Note":
                    project.notes[id].setValue(e[1]["data"])
            except :
                pass
        print(c)
    


   

    def get(self,url):
        #print("get")
        header = {"Authorization": "Bearer {}".format(self.ACCESS_TOKEN), 'Accept': 'application/json'}
        r = requests.get(url,headers=header)
        #print(r.text)
        if (r.status_code == 401):
            print("Token has expired")
            self.getAccessToken()
            return self.get(url)
        elif (r.status_code == 200):
            jsonData = json.loads(r.text)
            #print(url)
            return url,jsonData
        else :
            print(r.content)
            #print("Wrong param format")

    def load_url(self,url):
        print("load")
        header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0NzIxNjZiOC1hODUwLTExZWMtODgwYy0wMjQyYWMxMTAwMGEiLCJpc3MiOiJ3YW5nLnNob3RncmlkLmF1dG9kZXNrLmNvbSIsImF1ZCI6Indhbmcuc2hvdGdyaWQuYXV0b2Rlc2suY29tIiwiZXhwIjoxNjQ3NzgyOTI4LCJpYXQiOjE2NDc3ODIzMjgsInVzZXIiOnsidHlwZSI6IkFwaVVzZXIiLCJpZCI6NjB9LCJzdWRvX2FzX2xvZ2luIjpudWxsLCJhdXRoX3R5cGUiOiJhcGlfa2V5In0.xvp-kZYzCU_7ZYq9rozmEvgIuEzJ6QAlaU-VepcBMzE".format(), 'Accept': 'application/json'}
        r = requests.get(url,headers=header)
        print(r.text)
        return r.text

    def request(self,method,urls):

        out = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAXTHREAD) as executor:
            if method == "GET":
                future_to_url = (executor.submit(self.get,url) for url in urls)
            elif method == "POST":
                future_to_url = (executor.submit(self.post, url) for url in urls)
            elif method == "PATCH":
                future_to_url = (executor.submit(self.patch, url) for url in urls)
            
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    out.append(data)

        #print("out",data)
        return out             

    def multiFn(fn,input,workers=10000):
        #input : identity : inputData
        out = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAXTHREAD ) as executor:
            
            future_to_url = (executor.submit(fn,input[identity]) for identity in list(input.keys()))
           
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    out.append(data)
 
  
    


#request("GET",['https://wang.shotgrid.autodesk.com/api/v1/entity/projects/70/relationships/users'])
'''
    1. get target projectID
    2. find all human_users by relationship
        A
            1. for each user find his task by get following (filter by type&projectID)
            2. for each task find its data ex. duration, status, start-end
            3. visualize that data
        B
            1. for each user find his note by get following (filter by type&projectID)
            2. for each notes find its data relationship 
                => reply : writer content , attachment : img , link : thumbnail description creater 
            3. show that data
'''

'''
    1. get target projectID
    2. find all human_users by relationship
    3. for each user find his task by get following (filter by type&projectID)
    4. for each task find its data ex. duration, status, start-end
    5. visualize that data
     getTaskEntity(3588)
'''