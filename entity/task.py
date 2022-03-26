class Task:
    def __init__(self,id):
        self.id = id
        self.name = ""
        self.workload = ""
        self.status = ""
        self.dueDate = None
        self.content = ""
        self.startDate = None
        self.image = None
    
    def setValue(self,atrb):
        self.workload = atrb["workload"]
        self.status = atrb["sg_status_list"]
        self.dueDate = atrb["due_date"]
        self.startDate = atrb["start_date"]
        self.content = atrb["content"]
        self.name = atrb["cached_display_name"]
        self.image = atrb["image"]
    
    def print(self):
        print(self.workload,self.status,self.startDate,self.dueDate)
