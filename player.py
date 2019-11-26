import os
import requests
import json

from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd() + '/', '.env'))

# import url, token and player from .env file
url = os.environ['BASE_URL']
token = os.environ['TOKEN']
player = os.environ['PLAYER']



class Player:
    def __init__(self):
        self.player = player

    # keep looking until we land 
    # in a room with item to take
    def lookup_for_treasure(self):

    def go_to(self):
    
    def take(self):
