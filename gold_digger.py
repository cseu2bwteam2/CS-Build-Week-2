from apiCalls import APICalls


call = APICalls()

current_room = call.init()
print(current_room)

# track the gold qunatity we have
not_enough_gold = True