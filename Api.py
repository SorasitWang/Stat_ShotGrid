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

np.set_printoptions(threshold=2000)
class User:
    def __init__(self):
        self.profile = dict()
        #task
        self.tasksId = []
        self.tasksInfo = []

        self.statusStat = dict()
        self.statusStat["fin"] = 0
        self.statusStat["ip"] = 0
        self.statusStat["wtg"] = 0
        self.statusStat["none"] = 0

        self.contentStat = dict()

        self.workload = 0
        
        self.dateStat = dict()
        self.dateStat["timeline"] = np.array([0])
        now = datetime.datetime.now()
        self.dateStat["startEnd"] = \
            [datetime.date(now.year+10, 1, 1),datetime.date(now.year-10, 1, 1)]
        
        pass
    def print(self):
        print("Status",self.statusStat)
        print("Content",self.contentStat)
        print("Workload",self.workload)
        print("DateStat",self.dateStat)
        print("Range",np.shape(self.dateStat["timeline"]))
        print("---------------------------------------")
        
    def setTaskInfo(self,tasks : dict):

        print(len(self.tasksId))
        for id in self.tasksId:
            task = tasks.get(id)
            #status
            self.statusStat[task["sg_status_list"]] = 1 if task["sg_status_list"] not in self.statusStat \
                else self.statusStat[task["sg_status_list"]] + 1

            #content
            if (task["content"] == None):
                self.contentStat["none"] += 1
            else :
                self.contentStat[task["content"]] = 1 if task["content"] not in self.contentStat \
                    else self.contentStat[task["content"]] + 1

            #workload 
            self.workload += task["workload"]

            #date
            def changeDate(date):
                for d in date:
                    if d > self.dateStat["startEnd"][1]:
                        self.dateStat["startEnd"][1] = d
                    if d < self.dateStat["startEnd"][0]:
                        self.dateStat["startEnd"][0] = d
                    
            date = [task["start_date"],task["due_date"]]
            for i in range(0,2):
                    date[i] = date[i].split("-")
                    date[i] = datetime.date(int(date[i][0]),int(date[i][1]),int(date[i][2]))
          
            #print((self.dateStat["startEnd"][0]-date[0]).days)
            #return
            
            if len(self.dateStat["timeline"]) == 1:
                changeDate(date)
                r = self.dateStat["startEnd"][1]-self.dateStat["startEnd"][0]
                self.dateStat["timeline"] = np.array([1]*r.days)
            else :
                
                if date[0] < self.dateStat["startEnd"][0] :
                    #print(date[0],self.dateStat["startEnd"][0],np.shape(self.dateStat["timeline"]))
                    enlarge = np.array([1]*(self.dateStat["startEnd"][0]-date[0]).days)
                    self.dateStat["timeline"] = np.concatenate((enlarge,self.dateStat["timeline"]))
                    if date[1] < self.dateStat["startEnd"][0] :
                        changeDate(date)
                        continue
                if date[1] > self.dateStat["startEnd"][1] :
                    #print(date[1] , self.dateStat["startEnd"][1],np.shape(self.dateStat["timeline"]))
                    enlarge = np.array([1]*(date[1]-self.dateStat["startEnd"][1]).days)
                    self.dateStat["timeline"] = np.concatenate((self.dateStat["timeline"],enlarge))
                    if date[0] > self.dateStat["startEnd"][1] :
                        changeDate(date)
                        continue
                changeDate(date)
                idStart = date[0] - self.dateStat["startEnd"][0] 
                idEnd = date[1]-self.dateStat["startEnd"][0]
                #print(idStart,idEnd)
                self.dateStat["timeline"][idStart.days:idEnd.days+1] += 1
        pass
    
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

    

    def getAllUser(self,projectID):
        url = "{}/entity/projects/{}/relationships/users".format(self.URL,projectID)
        res = self.request("GET",[url])[0]
        re = []
        #print(res)
        for user in res[1]['data']:
            re.append(user['id'])
        #print(re)
        return re
    
    def getUserFollowing(self,users,type=None,projectId=None):
        urls =[]
        for id in users:
            #gen url
            urls.append("{}/entity/human_users/{}/following?entity={}&project_id={}"
                .format(self.URL,id,type.lower(),projectId))
        res = self.request("GET",urls)
        re = dict()
        allTask = []
        for e in res:
            #0 : url , 1 : data
            start = 60
            end = e[0].find("/",start+1)
            userId = int(e[0][start+1:end])
            tasks = []
            for entity in e[1]['data']:
                tasks.append(entity["id"])
            re[userId] = User()
            re[userId].tasksId = tasks
            allTask += tasks

            break
        # userId : User , [taskId]
        return  re ,allTask

    def getTaskInfo(self,tasks):
        urls = [ "{}/entity/Task/{}".format(self.URL,id) for id in tasks]
        res = self.request("GET",urls)
        re = dict()
        for e in res:
            start = len(self.URL)+12
            end = e[0].find("/",start+1) if e[0].find("/",start+1)!=-1 else len(e[0])+1
            id = int(e[0][start+1:end])
            #print(e[0],start,end,id)
            re[id] = e[1]["data"]["attributes"]
            
        #taskId : attributes
        return re 

   

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
            #print(jsonData)
            return url,jsonData
        else :
            pprint("Wrong param format")

    def load_url(self,url):
        print("load")
        header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0NzIxNjZiOC1hODUwLTExZWMtODgwYy0wMjQyYWMxMTAwMGEiLCJpc3MiOiJ3YW5nLnNob3RncmlkLmF1dG9kZXNrLmNvbSIsImF1ZCI6Indhbmcuc2hvdGdyaWQuYXV0b2Rlc2suY29tIiwiZXhwIjoxNjQ3NzgyOTI4LCJpYXQiOjE2NDc3ODIzMjgsInVzZXIiOnsidHlwZSI6IkFwaVVzZXIiLCJpZCI6NjB9LCJzdWRvX2FzX2xvZ2luIjpudWxsLCJhdXRoX3R5cGUiOiJhcGlfa2V5In0.xvp-kZYzCU_7ZYq9rozmEvgIuEzJ6QAlaU-VepcBMzE".format(), 'Accept': 'application/json'}
        r = requests.get(url,headers=header)
        print(r.text)
        return r.text

    def request(self,method,urls):

        out = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            
            future_to_url = (executor.submit(fn,input[identity]) for identity in list(input.keys()))
           
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    out.append(data)
   
a = Api()

a.getAccessToken()

ids = a.getAllUser(70)
userTasks,allTask = a.getUserFollowing(ids,"Task",70)
print(userTasks)
taskInfo = a.getTaskInfo(allTask)
#print(taskInfo)
#summarize taskinfo for each user
for info in userTasks.values():
    info.setTaskInfo(taskInfo)
    info.print()

#request("GET",['https://wang.shotgrid.autodesk.com/api/v1/entity/projects/70/relationships/users'])
'''
    1. get target projectID
    2. find all human_users by relationship
    3. for each user find his task by get following (filter by type&projectID)
    4. for each task find its data ex. duration, status, start-end
    5. visualize that data

     getTaskEntity(3588)




'''
