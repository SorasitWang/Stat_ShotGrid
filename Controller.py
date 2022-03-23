# This Python file uses the following encoding: utf-8

from api import Api
from entity.project import Project
class Controller:
    def __init__(self):
        pass

  
pMap = dict()
def init(op):
    a = Api()
    a.getAccessToken()
    pid = 70
    pMap[70] = Project(70)
    a.getAllUser(pMap[pid])

    def showTask():
        a.getUserFollowing(pMap[pid],"Task")
        taskInfo = a.getTaskInfo(pMap[pid])
       
        #summarize taskinfo for each user
        pMap[pid].summarize()
        

    def showNotes():
        userNotes,allNotes = a.getUserFollowing(pMap[pid],"Note")
        print(userNotes)

    if op=="T" :
        showTask()
    elif op=="N":
        showNotes()
init("T")