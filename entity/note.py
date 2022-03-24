from entity.link import Link
class Note:
    def __init__(self,id):
        self.id = id
        self.replies = []
        self.attachments = []
        self.description = None
        self.subject = None
        self.link = []
    
    def setValue(self,data):

        #print(data)
        rela = data["relationships"]
        atrb = data["attributes"]
        self.attachments = rela["note_links"]["data"]

        self.replies = rela["replies"]["data"]
        self.description = atrb["content"]
        self.subject = atrb["subject"]
       
        
    
    def print(self):
        print(self.attachments)
        print(self.replies)
        print("description",self.description)
        print("subject",self.subject)
        print("-----------------------")