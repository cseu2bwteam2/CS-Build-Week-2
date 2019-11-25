import os
import requests
import time
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

    def init(self):
        response = requests.get(url + '/adv/init/', headers={'Authorization': token}, json={"player": self.player}).json()

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
        response = requests.post(url + '/adv/move/', headers={'Authorization': token}, json={"direction": dir}).json()
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
        response = requests.post(url + '/adv/take/', headers={'Authorization': token}, json={"name": item}).json()
        try:
            print(response)
        except:
            print("Invalid response", response)
    def checkStatus(self):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        response = requests.post(url + '/adv/status/', headers={'Authorization': token}).json()
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

        response = requests.post(url + '/adv/sell/', headers={'Authorization': token}, json={"name": item, 'confirm': 'yes'}).json()
        try:
            print(response)
            self.status = response
        except:
            print("Invalid response", response)

    def getBalance(self):
        if self.waiting_time > time.time():
            time.sleep(self.waiting_time - time.time())
        
        response = requests.get(url + '/bc/get_balance/', headers={'Authorization': token}).json()
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
        
        response = requests.post(url + '/adv/move/', headers={'Authorization': token}, json={"direction":dir, "next_room_id": next_room}).json()
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
        
        response = requests.post(url + '/bc/get_balance/', headers={'Authorization': token}).json()
        try:
            print(response)
        except:
            print("Invalid response", response)

    



# c = APICalls()

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
