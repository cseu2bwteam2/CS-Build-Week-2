import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
from queue import Queue


token = os.getenv('TOKEN')
player_name = os.getenv('PLAYER_NAME')

def init_room():
    # Init
    response = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/adv/init/", json={
                            "player": player_name}, headers={'Authorization': token})
    

    data = response.json()
    print(data)

init_room()