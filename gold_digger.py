from apiCalls import APICalls
from player import Player

call = APICalls()
player = Player()

# current_room = call.init()
# print(current_room)

# track the gold qunatity we have
not_enough_gold = True

    while not_enough_gold:
        current_room = call.init()
        # if couldn't find the treasure, repeat
        while not player.lookup_for_treasure(current_room["room_id"], "tiny treasure"):
            current_room = call.init()
        current_room = call.init()
        player.travel(current_room["room_id"], "Shop")