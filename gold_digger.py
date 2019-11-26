from apiCalls import APICalls
from player import Player
from time import sleep


call = APICalls()
player = Player()

# track the gold qunatity we have
not_enough_gold = True

while not_enough_gold:
    current_room = call.init()
    # if couldn't find the treasure, repeat
    while not player.lookup_for_treasure(current_room["room_id"], "tiny treasure"):
        current_room = call.init()
    current_room = call.init()
    # Picked something will go sellling it 
    player.travel(current_room["room_id"], "Shop")
    
    # sell the treasure
    response = call.sell("tiny treasure")

    # relax a bit
    sleep(response["cooldown"])

    gold = response["gold"]

    print("******  Sold a coin  ******")
    print("******  You have "+str(gold)+" gold coins  ******")
    
    if int(gold) >= 1000:
        not_enough_gold = False