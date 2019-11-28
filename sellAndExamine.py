import os
import requests
import time
import hashlib
import json
import random
from time import sleep
from apiCalls import APICalls
from jump_to_room import jump_to_room

calls = APICalls()
calls.init()

def sell():
        jump_to_room('1')
        calls.checkStatus()
        while len(calls.status['inventory']):
                calls.sell(calls.status['inventory'][0])
                calls.checkStatus()

def changeName(name):
        jump_to_room('467')
        calls.change_player_name(name)

# it saves the binary code to a file(des description.py) 
def examine():
        jump_to_room('55')
        calls.examine()


# once the gold digger is done hunting for 
# treasures, we sell them for gold
# then change player name to be able to mine coins
sell()
changeName('obama')
examine()