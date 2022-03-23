class Project:
    def __init__(self,id):
        self.users = dict()
        self.id = id
        self.tasks = dict()
        self.tasksList = []
        self.notes = dict()
        pass
    
    def summarize(self):
        for u in self.users.values():
            u.summarizeTask()
            u.print()