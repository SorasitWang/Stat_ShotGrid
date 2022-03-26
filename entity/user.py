from entity.task import Task
from asyncio.windows_events import NULL
import requests
from dotenv import load_dotenv
import datetime
import numpy as np

class User:
    def __init__(self,id):
        self.profile = dict()
        self.id = id
        #task
        self.tasks = dict()
        self.notes = dict()
        self.tasksId = []
        self.tasksInfo = []
        self.firstName = ""
        self.lastName = ""
        self.image = "./res/profile.jpg"
        self.email = ""
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
        
        #note
        
        pass
    def print(self,type=None):
        print(self.id)
        if type==None or type=="Task" :
            print("Status",self.statusStat)
            print("Content",self.contentStat)
            print("Workload",self.workload)
            print("DateStat",self.dateStat)
            print("Range",np.shape(self.dateStat["timeline"]))
            print("---------------------------------------")
        if type==None or type=="Note":
            for n in self.notes.values():
                n.print()
    def setAtrb(self,atrb):
        self.firstName = atrb["firstname"]
        self.lastName = atrb["lastname"]
       
        self.image = atrb["image"]
        self.email = atrb["email"]
    def summarizeTask(self):

        print(len(self.tasksId))
        for task in self.tasks.values():
            #status
            self.statusStat[task.status] = 1 if task.status not in self.statusStat \
                else self.statusStat[task.status] + 1

            #content
            if (task.content == None):
                self.contentStat["none"] += 1
            else :
                self.contentStat[task.content] = 1 if task.content not in self.contentStat \
                    else self.contentStat[task.content] + 1

            #workload 
            self.workload += task.workload

            #date
            def changeDate(date):
                for d in date:
                    if d > self.dateStat["startEnd"][1]:
                        self.dateStat["startEnd"][1] = d
                    if d < self.dateStat["startEnd"][0]:
                        self.dateStat["startEnd"][0] = d
                    
            date = [task.startDate,task.dueDate]
            
            for i in range(0,2):
                    date[i] = date[i].split("-")
                    date[i] = datetime.date(int(date[i][0]),int(date[i][1]),int(date[i][2]))
            changeDate(date)
        
        r = self.dateStat["startEnd"][1]-self.dateStat["startEnd"][0]
        self.dateStat["timeline"] = np.array([0]*(r.days+1))

        for task in self.tasks.values():
            date = [task.startDate,task.dueDate]
            
            for i in range(0,2):
                    date[i] = date[i].split("-")
                    date[i] = datetime.date(int(date[i][0]),int(date[i][1]),int(date[i][2]))
            idStart = date[0] - self.dateStat["startEnd"][0] 
            idEnd = date[1]-self.dateStat["startEnd"][0]
            self.dateStat["timeline"][idStart.days:idEnd.days+1] += 1
        pass
 