class Link:
    def __init__(self):
        self.imageURL = None
        self.description = None
        self.creator = None
        pass

    def setAtrb(self,attributes):
        self.imageURL = attributes.image
        self.description = attributes.description
    
    def setRelation(self):
        pass
        