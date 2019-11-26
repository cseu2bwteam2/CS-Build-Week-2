from apiCalls import APICalls


call = APICalls()

current_room = call.init()
print(current_room)