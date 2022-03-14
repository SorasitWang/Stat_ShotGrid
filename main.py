from dotenv import load_dotenv
import os
import shotgun_api3
from pprint import pprint # useful for debugging

load_dotenv()
sg = shotgun_api3.Shotgun("https://wang.shotgrid.autodesk.com",
                          script_name=os.getenv('SCRIPT_NAME'),
                          api_key=os.getenv('API_KEY'))
result = sg.find('Project',[])
pprint(result)