import os
import requests
import json
from apiCalls import APICalls
from queue import Queue

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

    # keep looking until we land 
    # in a room with item to take
    def lookup_for_treasure(self, current_room_id, item, fly = False, dash = False):
        rooms_data = []
        with open("room_data_copy.py", "r") as f:
            rooms_data = json.loads(f.read())

        # Go to item
        self.travel(current_room_id, item, fly, dash)
        # Pick up item
        data = self.call.take()
        # their was a successful pickup
        if data:
            # pause to cool
            # sleep(data["cooldown"])
            # Remove item from rooms_data
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

    def travel(self, destination, current_room_id, fly = False, dash = False):
        room_data = []
        room_directions = {}
        # read the files
        with open("room_data_copy.py", "r") as f:
            room_data = json.loads(f.read())
        with open("room_graph_copy.py", "r") as f:
            room_directions = json.loads(f.read())
        
        # Another traversal
        traverse = traverse_path(room_directions, room_data, current_room_id, destination)
        # Could not get there
        if not traverse:
            print("Could not find a way to " +str(destination)")
            return
        # Found a way
        for step in range(len(traverse)):
            data = {}
            flew = False
            dashed = False
            if fly:
                for room in room_data:
                    if str(room['room_id']) == current_room_id:
                        # we fly to get up faster
                        if room['terrain'].lower() == "elevated" and 'terrain' in room:
                            data = APICalls.flight(traverse[step])
                            used_flight = True
                            break
                        else:
                            break
            # dash if can dash and didn't use fly and there is more rooms to dash through than 1
            if not flew and dash:
                dash_destination = [traverse[step]]
                jump = step + 1
                while jump < len(traverse):
                    if traverse[jump] == dash_destination[jump - 1]:
                        dash_destination.append(traverse[jump])
                    else:
                        break
                if len(dash_destination) > 1:
                    traversed_id = []
                    flip_room = current_room_id
                    for direction in dash_destination:
                        traversed_id.append(room_map[flip_room][direction])
                        flip_room = room_map[flip_room][direction]
                    num_of_rooms = len(traversed_id)
                    traversed_id = ','.join(traversed_id)
                    data = APICalls.dash(traverse[step], num_of_rooms, traversed_id)
                    step += len(dash_destination) - 1
                    dashed = True                    
            # boring walking
            if not dashed and not flew:
                next_room_id = room_directions[current_room_id][traverse[step]]
                data = APICalls.move(traverse[step])

            current_room_id = str(data['room_id'])
            sleep(data["cooldown"])
            print(data)

    def traverse_path(self, room_directions, room_data, room_id, destination):
        q = Queue()
        explored = set()
        ways = {}
        q.enqueue(room_id)
        ways[room_id] = [room_id]
        # the usual usual
        while q.size() > 0:
            current_room = q.dequeue()
            explored.add(current_room)
            for room_lookup in room_map[current_room].values():
                if room_lookup in explored or room_lookup == '?':
                    continue
                # flipping
                new_way = ways[current_room][:]
                new_way.append(room_lookup)
                ways[room_lookup] = new_way
                found = False
                for data in room_data:
                    if room_lookup == str(data['room_id']):
                        # check the room title if it match
                        if data['title'].lower() == destination.lower():
                            found = True
                            break
                        # check the room itmes if it match
                        if 'items' in data and destination in data['items']:
                            found = True
                            break
                if room_lookup == destination:
                    # we found the room
                    found = True
                if found:
                    the_way = ways[room_lookup]
                    exits = []
                    for step in range(len(the_way) - 1):
                        exits.append(directionToRoom(
                            room_map, the_way[step], the_way[step + 1]))
                    return exits
                q.enqueue(room_lookup)
        return None