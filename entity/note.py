
from entity.link import Link
import api as api
class Note:
    def __init__(self,id,project):
        self.id = id
        self.replies = []
        self.links = dict()
        self.description = None
        self.subject = None
        self.link = []
        self.project = project
        self.api = api.Api()
    
    def setValue(self,data):
        
        #print(data)
        rela = data["relationships"]
        atrb = data["attributes"]
        links = rela["note_links"]["data"]
        #!! assume all link is Shot !!
        for l in links :
            if l["type"] == "Shot" :
                tmp = Link(l,self.project)
                self.links[l["id"]] = tmp
                self.project.links[l["id"]] = tmp
        self.replies = rela["replies"]["data"]
        self.description = atrb["content"]
        self.subject = atrb["subject"]
       
        
    
    def print(self):
        return
        print(self.attachments)
        print(self.replies)
        print("description",self.description)
        print("subject",self.subject)
        print("-----------------------")