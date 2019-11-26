import requests
import time
import os
from jump_to import jump_to_room
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd() + '/', '.env'))

baseUrl = os.environ['BASE_URL']
token = os.environ['TOKEN']
player = os.environ['PLAYER']

auth = {"Authorization": token}


def get_current_room():
    print(baseUrl + "/adv/init/")
    res = requests.get(
        baseUrl + "/adv/init/",
        headers=auth
    )
    res_json = res.json()
    time.sleep(res_json["cooldown"])
    return res_json["room_id"]


def change_player_name():
    res = requests.post(
        baseUrl + "/adv/change_name/",
        headers=auth,
        json={"name": player, "confirm": "aye"}
    )
    return res.json()


if __name__ == "__main__":
    current_room = get_current_room()
    jump_to_room('467', current_room)
    response = change_player_name()
    print(response)
