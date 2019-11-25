import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
from queue import Queue


# Read the credential from the .env file
token = os.getenv('TOKEN')
player_name = os.getenv('PLAYER_NAME')


def init_room():
    # Init
    response = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/adv/init/", json={
                            "player": player_name}, headers={'Authorization': token})
    data = response.json()

    # intialise with empty data
    rooms_data = []
    # append with the received data
    rooms_data.append(data)

    # write the data to the file, it will be used as 
    # starting point
    with open("rooms_data.py", "w") as rooms:
        rooms.write(json.dumps(rooms_data))


init_room()

