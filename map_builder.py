import requests
import json
# from dotenv import load_dotenv
# load_dotenv()
# import os
from queue import Queue


# token = os.getenv('TOKEN')

def init_room():
    # Init
    response = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/adv/init/", json={
                            "player": "player375"}, headers={'Authorization': "Token 5b68275223b5774b6a277c8a21b18c4629540e1c"})
    

    data = response.json()
    print(data)


init_room()