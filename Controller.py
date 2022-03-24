# This Python file uses the following encoding: utf-8


import entity.project as p
import api as api
class Controller:
    def __init__(self):
        pass

  
pMap = dict()
def init(op):
    a = api.Api()
    a.getAccessToken()
    pid = 70
    pMap[70] = p.Project(70)
    a.getAllUser(pMap[pid])

    def showTask():
        a.getUserFollowing(pMap[pid],"Task")
        a.getInfo(pMap[pid],"Task","attributes")
        #summarize taskinfo for each user
        pMap[pid].summarize()
        

    def showNotes():
        a.getUserFollowing(pMap[pid],"Note")
        a.getInfo(pMap[pid],"Note","relationships")
        for u in pMap[pid].users.values():
            u.print("Note")

    if op=="T" :
        showTask()
    elif op=="N":
        showNotes()
init("N")