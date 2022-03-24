class Link:
    def __init__(self,data,project):
        #set data from realtionships
        self.id = data["id"]
        self.name = data["name"]
        self.type = data["type"]
        self.project = project
        self.imageURL = None
        self.description = None

        pass

    def setAtrb(self,attributes):
        self.imageURL = attributes["image"]
        self.description = attributes["description"]

    def print(self):
        print(self.name)
        print(self.imageURL)
        print(self.description)
        print("------------------")

#https://stackoverflow.com/questions/68104165/display-image-from-url
        