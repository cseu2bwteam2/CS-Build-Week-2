import requests
import time
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd() + '/', '.env'))

from goto import goto
baseUrl = os.environ['BASE_URL']
token = os.environ['TOKEN']
player = os.environ['PLAYER']


auth = {"Authorization": token}


def get_current_room():
    res = requests.get(
        baseUrl + "/adv/init/",
        headers=auth
    )
    res_json = res.json()
    print(res_json)
    time.sleep(res_json["cooldown"])
    return res_json["room_id"]


def change_player_name():
    res = requests.post(
        baseUrl + "/adv/change_name/",
        headers=auth,
        json={"name": player, "confirm": "yes"}
    )
    return res.json()


if __name__ == "__main__":
    current_room = get_current_room()
    print(current_room, 'currrr')
    change_name_room = "467"
    # goto(str(current_room), change_name_room)
    response = change_player_name()
    print(response)
