import requests
from time import sleep
import json
from dotenv import load_dotenv
load_dotenv()
import os
from util import Queue
load_dotenv(os.path.join(os.getcwd() + '/', '.env'))

# Read the credential from the .env file
token = os.getenv('TOKEN')
player_name = os.getenv('PLAYER')
# directions to comeback
go_back = {"n": "s", "s": "n", "e": "w", "w": "e"}


def init_room():
    # intialise with empty data
    rooms_data = []
    # Load the starting room
    start_room = {  "room_id": 0,
                    "title": "Room 0",
                    "description": "You are standing in an empty room.",
                    "coordinates": "(60,60)",
                    "players": [],
                    "items": ["small treasure"],
                    "exits": ["n", "s", "e", "w"],
                    "cooldown": 60.0,
                    "errors": [],
                    "messages": []
                }
    rooms_data.append(start_room)

    # write the data to the file, it will be used as 
    # starting point
    with open("rooms_data.py", "w") as rooms:
        rooms.write(json.dumps(rooms_data))

    # intialise with empty directions
    rooms_directions = {}
    # initialise the direction with the current room
    # intial room ID is "0"
    room_init = {"0": {"n": "?", "s": "?", "e": "?", "w": "?"}}
    rooms_directions.update(room_init)
    # write to the file
    with open("rooms_directions.py", "w") as rooms:
        rooms.write(json.dumps(rooms_directions))


def room_walker(queue):
    # get the current room id
    room_id = str(rooms_data[-1]["room_id"])

    # pull possible direction from this room
    current_directions = rooms_directions[room_id]
    # track the path that have not been visited yet
    not_visited_paths = []
    # loop through current room
    for direction in current_directions:
        # if that direction is still at '?'
        # then it is unexplored
        if current_directions[direction] == '?':
            # add it to the (not visited)paths
            not_visited_paths.append(direction)
    # if some rooms have not been explored yet
    if not_visited_paths:
        # add to the queue
        queue.enqueue(not_visited_paths[0])
    else:
        # keep looking for not visited room
        # BFT traversal 
        unexplored_path = BF_traversal(rooms_data, rooms_directions)
        # if there are rooms that have not been visited
        if unexplored_path is not None:
            # explore the path
            for path in unexplored_path:
                for direction in current_directions:
                    # if the direction is a match
                    # we enqueue
                    if current_directions[direction] == path:
                        queue.enqueue(direction)


def BF_traversal(rooms_data, rooms_directions):
    # New local queue
    q = Queue()
    # enqueue the current room as a list
    q.enqueue([str(rooms_data[-1]["room_id"])])

    # track the visited room
    visited_room = set()

    # Our classical while loop
    while q.size() > 0:
        # get the rooms list
        rooms_list = q.dequeue()
        # pull in a room
        room = rooms_list[-1]

        # if the room has not been visited
        if room not in visited_room:
            # we add it
            visited_room.add(room)
            # loop through the possible directions of the room
            for direction in rooms_directions[room]:
                # if not visited we 
                # return the current room list
                if rooms_directions[room][direction] == '?':
                    return rooms_list
                else:
                    path = list(rooms_list)
                    # add the direction to the path
                    path.append(rooms_directions[room][direction])
                    # enqueue it
                    q.enqueue(path)
    # return None if no unexplored room is found
    return None

# Itnitalise to the starting room
# Write to the files for mapping
init_room()

# read the rooms data file
with open("rooms_data.py", "r") as rooms:
    # read the room details
    rooms_data = json.loads(rooms.read())
# read the rooms directions file
with open("rooms_directions.py", "r") as directions:
    # read the map from the room_graph world
    rooms_directions = json.loads(directions.read())

# create a queue
queue = Queue()

# call room_walker with queue and related files
room_walker(queue)

# While we have room in the queue to visit
while queue.size() > 0:
    # read the rooms data file
    with open("rooms_data.py", "r") as rooms:
        # read the room details
        rooms_data = json.loads(rooms.read())

    # read the directions file
    with open("rooms_directions.py", "r") as directions:
        # read the map from the room_graph world
        rooms_directions = json.loads(directions.read())

    # get the room where the player is
    player_room = str(rooms_data[-1]["room_id"])
    # Where he go next from the queue
    direction = queue.dequeue()
    # get the player moving
    response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json={"direction": direction}, headers={'Authorization': token})
    # parse the response
    data = response.json()
    # add to the rooms_data
    rooms_data.append(data)

    #####print(rooms_data)
    # updated position
    updated_room = str(rooms_data[-1]["room_id"])
    print("moved to room " + str(updated_room))
    # update the map 
    rooms_directions[player_room][direction] = updated_room
    # if the room not on the map yet
    if updated_room not in rooms_directions:
        exits = data["exits"]
        directions = {}
        for door in exits:
            directions[door] = "?"
        rooms_directions[updated_room] = directions

    # come back to the the previous room
    back = go_back[direction]
    # point the destination room to the previous room
    rooms_directions[updated_room][back] = player_room

    # update the directions file
    with open("rooms_directions.py", "w") as directions:
        directions.write(json.dumps(rooms_directions))
    # update the rooms data file
    with open("rooms_data.py", "w") as rooms:
        rooms.write(json.dumps(rooms_data))
    # pause while cooling down
    sleep(data["cooldown"])
    # Then walk again
    room_walker(queue)