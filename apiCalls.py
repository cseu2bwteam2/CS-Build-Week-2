import os
import requests
import time
import hashlib
import json
import random

from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd() + '/', '.env'))


# import url, token and player from .env file
url = os.environ['BASE_URL']
token = os.environ['TOKEN']
player = os.environ['PLAYER']


class APICalls:
    def __init__(self):
        self.player = player
        self.waiting_time = 0
        self.current_room = {}
        self.status = {}
        self.new_proof = 0

    def init(self):
        response = requests.get(
            url + '/adv/init/', headers={'Authorization': token}, json={"player": self.player}).json()

        try:
            self.waiting_time = time.time() + float(response.get('cooldown'))
            self.current_room = response
        except:
            print("Invalid response", response)

    def move(self, dir):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        if dir not in self.current_room['exits']:
            print('You cant move')
            return
            print(url)
        response = requests.post(
            url + '/adv/move/', headers={'Authorization': token}, json={"direction": dir}).json()
        try:
            self.waiting_time = time.time() + float(response.get('cooldown'))
            self.current_room = response
            print(self.current_room)
        except:
            print("Invalid response", response)

    def take(self, item='tiny_treasure'):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        if item not in self.current_room['items']:
            print('No items')
            return
        response = requests.post(
            url + '/adv/take/', headers={'Authorization': token}, json={"name": item}).json()
        try:
            print(response)
        except:
            print("Invalid response", response)

    def checkStatus(self):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        response = requests.post(url + '/adv/status/',
                                 headers={'Authorization': token}).json()
        try:
            print(response)
            self.status = response
        except:
            print("Invalid response", response)

    def sell(self, item='tiny_treasure'):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        if self.current_room['title'] != 'Shop' or self.status['inventory'].length < 1:
            print('Unable to sell treasure')
            return

        response = requests.post(
            url + '/adv/sell/', headers={'Authorization': token}, json={"name": item, 'confirm': 'yes'}).json()
        try:
            print(response)
            self.status = response
        except:
            print("Invalid response", response)

    def getBalance(self):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        response = requests.get(url + '/bc/get_balance/',
                                headers={'Authorization': token}).json()
        try:
            print(response)
        except:
            print("Invalid response", response)

    def wiseExplorer(self, dir, next_room):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        if dir not in self.current_room['exits']:
            print('You cant move')
            return

        response = requests.post(url + '/adv/move/', headers={'Authorization': token}, json={
                                 "direction": dir, "next_room_id": next_room}).json()
        try:
            self.waiting_time = time.time() + float(response.get('cooldown'))
            self.current_room = response
        except:
            print("Invalid response", response)

    def pray(self):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        if self.current_room['title'] != 'Shrine':
            print('You are not in a shrine')
            return

        response = requests.post(
            url + '/bc/get_balance/', headers={'Authorization': token}).json()
        try:
            print(response)
            self.waiting_time = time.time() + float(response.get('cooldown'))
        except:
            print("Invalid response", response)

    def valid_proof(self, block_string, proof, difficulty):
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # print('0' * difficulty)
        # print(guess_hash[:difficulty])
        return guess_hash[:difficulty] == "0" * difficulty

    def proof_of_work(self, block, difficulty):

        block_string = json.dumps(block, sort_keys=True).encode()
        proof = 0
        while self.valid_proof(block_string, proof, difficulty) is False:
            proof = random.getrandbits(64)
            print(proof)
        self.new_proof = proof
        print(proof)
        if (self.new_proof > 0):
            return self.mineCoin(proof)

    def mineCoin(self, proof):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        response = requests.post(
            url + '/bc/mine/', headers={'Authorization': token}, json={"proof": int(proof)})
        if response.status_code == 400:
            self.new_proof = 0
        response = response.json()
        print(response)

        return response
        # try:
        #     print(response)
        #     self.waiting_time = time.time() + float(response.get('cooldown'))
        # except:
        #     print('Invaleid response', response)

    def examine(self, item_or_player):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        response = requests.post(
            url + '/adv/examine/', headers={'Authorization': token}, json={"name": item_or_player}).json()
        try:
            print(response)
            self.waiting_time = time.time() + float(response.get('cooldown'))
        except:
            print('Invaleid response', response)

    def equipment(self, wearables):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        response = requests.post(
            url + '/adv/wear/', headers={'Authorization': token}, json={"name": wearables}).json()
        try:
            print(response)
            self.waiting_time = time.time() + float(response.get('cooldown'))
        except:
            print('Invaleid response', response)

    def flight(self, dir):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        response = requests.post(
            url + '/adv/fly/', headers={'Authorization': token}, json={"direction": dir}).json()
        try:
            self.waiting_time = time.time() + float(response.get('cooldown'))
            self.current_room = response
            print(self.current_room)
        except:
            print("Invalid response", response)

    def carry(self, item):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        response = requests.post(
            url + '/adv/carry/', headers={'Authorization': token}, json={"name": item}).json()
        try:
            print(response)
            self.waiting_time = time.time() + float(response.get('cooldown'))
        except:
            print('Invaleid response', response)

    def receive(self, item):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        response = requests.post(
            url + '/adv/recieve/', headers={'Authorization': token}).json()
        try:
            print(response)
            self.waiting_time = time.time() + float(response.get('cooldown'))
        except:
            print('Invaleid response', response)

    def transmogrify(self, item):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())

        response = requests.post(
            url + '/adv/transmogrify/', headers={'Authorization': token}, json={"name": item}).json()
        try:
            print(response)
            self.waiting_time = time.time() + float(response.get('cooldown'))
        except:
            print('Invaleid response', response)

    def dash(self, dir, num_of_rooms, next_rooms):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        if dir not in self.current_room['exits']:
            print('You cant move')
            return

        response = requests.post(url + '/adv/dash/', headers={'Authorization': token}, json={
                                 "direction": dir, "num_rooms": num_of_rooms, "next_room_ids": next_rooms}).json()

        try:
            self.waiting_time = time.time() + float(response.get('cooldown'))
            self.current_room = response
            print(self.current_room)
        except:
            print("Invalid response", response)

    def get_current_room(self):
        res = requests.get(
            url + "/adv/init/",
            headers={'Authorization': token}
        )
        res_json = res.json()
        time.sleep(res_json["cooldown"])
        return res_json["room_id"]

    def change_player_name(self):
        res = requests.post(
            url + "/adv/change_name/",
            headers={'Authorization': token},
            json={"name": player, "confirm": "aye"}
        )
        print(res.json())
        return res.json()


response = requests.get(
    url + '/bc/last_proof/', headers={'Authorization': token}).json()
print(response)
block = response['proof']
difficulty = response['difficulty']
c = APICalls()
while True:
    res = c.proof_of_work(response['proof'], response['difficulty'])
    time.sleep(res["cooldown"])



# c.init()
# c.move('s')
# c.move('e')
# c.move('w')
# c.move('d')
# c.take()
# c.checkStatus()
# c.sell()
# c.getBalance()
# c.pray()
# c.move('n')
# c.move('s')
# c.move('w')
# c.move('e')
# c.flight('e')
