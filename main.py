from dotenv import load_dotenv
import os
import shotgun_api3
from pprint import pprint # useful for debugging
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import concurrent.futures
import requests
import time

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))





def multiReq():


    out = []
    CONNECTIONS = 100
    TIMEOUT = 5

    #tlds = open('../data/sample_1k.txt').read().splitlines()
    urls = ['https://wang.shotgrid.autodesk.com/api/v1/entity/projects/70/relationships/users']

    def load_url(url, timeout):
        
        header = header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJkNDg2ZDlmZS1hODRlLTExZWMtYTExMi0wMjQyYWMxMTAwMDIiLCJpc3MiOiJ3YW5nLnNob3RncmlkLmF1dG9kZXNrLmNvbSIsImF1ZCI6Indhbmcuc2hvdGdyaWQuYXV0b2Rlc2suY29tIiwiZXhwIjoxNjQ3NzgyMzA2LCJpYXQiOjE2NDc3ODE3MDYsInVzZXIiOnsidHlwZSI6IkFwaVVzZXIiLCJpZCI6NjB9LCJzdWRvX2FzX2xvZ2luIjpudWxsLCJhdXRoX3R5cGUiOiJhcGlfa2V5In0.JMU90lXMc2jMj4lpS6Qk0rSWwsZh5OmShCA-1FwpVtg".format(), 'Accept': 'application/json'}
        r = requests.get(url,headers=header)
        
        return r.text

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                out.append(data)

                print(str(len(out)),end="\r")

        time2 = time.time()

    print(f'Took {time2-time1:.2f} s')
    print(out)
multiReq()
'''
app = QtWidgets.QApplication([])
widget = MyWidget()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec_())
'''

'''
sg = shotgun_api3.Shotgun("https://wang.shotgrid.autodesk.com",
                          script_name=os.getenv('SCRIPT_NAME'),
                          api_key=os.getenv('API_KEY'))
                          
filter = [
        ['project', 'is', {'type': 'Project', 'id': 70}],
        ['sg_status_list','is', "ip"],
        ['assgined_to','is',""]

        #['tasks','is',{'type': 'Task', 'id': 5097}]
        ]

def main():
    user = {"type": "HumanUser", "id": 17}
    project = {"type": "Project", "id": 70}
    entity_type =  "Task"
    #pprint(sg)

    result = sg.following(user, project=project, entity_type=entity_type)
    #pprint(result)


    #filter = [['playlist', 'is', {'type':'Playlist', 'id':6}]]
    fields = ['due_date']

    result = sg.find("Task",filter,fields)
    pprint(result)


    result = sg.followers({"type": "Task", "id": 3588})


    result = sg.followers({"type": "Shot", "id": 863})'''
    #pprint(result)
