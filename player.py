import os
import requests
import json
from apiCalls import APICalls

from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd() + '/', '.env'))

# import url, token and player from .env file
url = os.environ['BASE_URL']
token = os.environ['TOKEN']
player = os.environ['PLAYER']

class Player:
    def __init__(self):
        self.player = player
        self.call = APICalls()
        self.room = self.call.init()

    # keep looking until we land 
    # in a room with item to take
    def lookup_for_treasure(self):
        rooms_data = []
        with open("room_details_copy.py", "r") as f:
            rooms_data = json.loads(f.read())

        # Go to item
        self.go_to(current_room_id, item_name, can_fly, can_dash)
        # Pick up item
        data = self.call.take()
        # their was a successful pickup
        if data:
            # pause to cool
            # sleep(data["cooldown"])
            # Remove item from rooms_data
            current_room_id = self.room["room_id"]
            for room in rooms_data:
                # find the matching room
                if str(rooms['room_id']) == current_room_id:
                    if len(room['items']) > 0:
                        # since we can only have one item at 
                        # a time in items list, we can empty it
                        room['items'] = []
            # update the file
            with open("rooms_data_copy.py", "w") as f:
                f.write(json.dumps(rooms_data))
            print(f"\n******  Picked up {data["items"][0]}  ******\n")
            return True
        # no item was picked
        return False


    def go_to(self):
    
    def take(self):
