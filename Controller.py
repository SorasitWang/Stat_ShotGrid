# This Python file uses the following encoding: utf-8


import entity.project as p
import api as api
class Controller:
    
       
    def __init__(self):
        self.a = api.Api()
        self.a.getAccessToken()
        ids = self.a.initProjects()
        self.projects = dict()
        print(ids)
        for i in ids :
            self.projects[i] = p.Project(i)
        self.pid = 70
        #pMap[70] = p.Project(70)
        self.a.getAllUser(self.projects[self.pid])
        self.a.getInfo(self.projects[self.pid],"Human_Users")

    def getUsers(self):
        return self.projects[self.pid].users
    def getAllIds(self):
        return self.projects.keys()
    def selectProject(self,id):
        self.pid = id

    def showTask(self):
        self.a.getUserFollowing(self.projects[self.pid],"Task")
        self.a.getInfo(self.projects[self.pid],"Task","attributes")
        #summarize taskinfo for each user
        self.projects[self.pid].summarize()
            

    def showNotes(self):
        self.a.getUserFollowing(self.projects[self.pid],"Note")
        self.a.getInfo(self.projects[self.pid],"Note","relationships")
        for u in self.projects[self.pid].users.values():
            u.print("Note")
        '''
        if op=="T" :
            showTask()
        elif op=="N":
            showNotes()
        '''


