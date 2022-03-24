from api import Api
class Project:
    def __init__(self,id):
        self.users = dict()
        self.id = id
        self.tasks = dict()
        self.tasksList = []
        self.notes = dict()
        self.links = dict()
        self.api = Api()
        pass
    
    def summarize(self):
        for u in self.users.values():
            u.summarizeTask()
            u.print()
    def getLinksValue(self):
        self.api.getInfo(self,"Shot")
        for l in self.links.values() :
            l.print()