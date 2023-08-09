import random
import yaml
import pickle
import battle
import os

# says you are not playing.
play = 0

fought_enemy = False

# opens data files
with open("map.yaml") as f:
    map = yaml.safe_load(f)

with open("items.yaml") as f:
    item = yaml.safe_load(f)

with open("start.yaml") as f:
    start_player = yaml.safe_load(f)

create_save = input("Do you want to [o]pen saved game or create [n]ew game? ")

if create_save.lower().startswith('n'):
    enter_save_name = input("Please name your save: ")
    player = start_player
    dumped = yaml.dump(player)
    save_name = "save_" + enter_save_name + ".yaml"
    with open(save_name, "w") as f:
        f.write(dumped)
    save_file = save_name
    play = 1
elif create_save.lower().startswith('o'):
    open_save = input("Please choose a save to open: ")
    save_file = "save_" + open_save + ".yaml"
    check_file = os.path.isfile(save_file)
    if check_file == False:
        print("ERROR: Couldn't find save file '" + save_file + "'")
        exit(1)
    with open(save_file) as f:    
        player = yaml.safe_load(f)
    play = 1
else:
    print("ERROR: That option is not allowed.")

# you died
def die():
    if player["cheat"] < 3:
        cheatcode = input("What is the not-die code?")
        if not cheatcode == 43590:
            player = start_player
        else:
            player["cheat"] += 1
            player["health"] = player["max helth"]
    else:
        print("You've cheated too much! No more lives!")
        player = start_player

# funcion to search through the map file
def search(x, y):
    global map_loaction
    for i in range(0, map["coordinate count"]):
        if map["point" + str(i)]["x"] == player["x"] and map["point" + str(i)]["y"] == player["y"]:
            map_loaction = i
            break
        else:
            quit_tp = input("ERROR: You are in an undefined position. This could be because you are using a different map file, or you edited your save file. Do you want to quit or teleport to point0?")
            if quit_tp.lower().startswith('t'):
                player["x"] = map["point0"]["x"]
                player["y"] = map["point0"]["y"]
                map_loaction = 0
            else:
                print("Quitting...")

# gameplay here:
def run(play):
    print("Reserved keys:")
    print("N: Go north")
    print("S: Go south")
    print("E: Go east")
    print("W: Go west")
    print("If you find an item on the ground, type the name of the item to take it.")
    print("I: view items. When in this view, type the name of an item to examine it.")
    print("Some items have special triggers, wich will often be stated in the description. Others can only be activated in certain situations, like in combat.")
    # Mapping stuff

    while play == 1:
        search(player["x"], player["y"])
        global map_loaction
        print(map_loaction)
        if "North" not in map["point" + str(map_loaction)]["blocked"]:
            print("You can go North")
        if "South" not in map["point" + str(map_loaction)]["blocked"]:
            print("You can go South")
        if "East" not in map["point" + str(map_loaction)]["blocked"]:
            print("You can go East")
        if "West" not in map["point" + str(map_loaction)]["blocked"]:
            print("You can go West")
        if "None" not in map["point" + str(map_loaction)]["item"]:
            print("There are these items on the ground: ", map["point" + str(map_loaction)]["item"])
        if map["point" + str(map_loaction)]["enemy"] > 0 and map_loaction not in player["defeated enemies"]:
            enemies_remaining = map["point" + str(map_loaction)]["enemy"]
            while enemies_remaining > 0:
                battle.fight()
                enemies_remaining -= 1
            if player["health"] > 0:
                player["defeated enemies"].append(map_loaction)
            else:
                die()
        command = input("What will you do?")
        if command.lower().startswith('go'):
            print("Rather than saying Go <direction>, simply say <direction>.")
        elif command.lower().startswith('n'):
            if "North" in map["point" + str(map_loaction)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["y"] += 1
                # search(player["x"], player["y"])
        elif command.lower().startswith('s'):
            if "South" in map["point" + str(map_loaction)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["y"] -= 1
        elif command.lower().startswith('e'):
            if "East" in map["point" + str(map_loaction)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["x"] += 1
        elif command.lower().startswith('w'):
            if "West" in map["point" + str(map_loaction)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["x"] -= 1
        elif command.lower().startswith('i'):
            which_item = input("You have these items in your inventory: " + str(player["inventory"]))
            if which_item in player["inventory"]:
                print(item[which_item]["description"])
        elif command in map["point" + str(map_loaction)]["item"]:
            if command not in player["inventory"]:
                player["inventory"].append(command)
            else:
                print("You already have that item.")
        elif command.lower().startswith('q'):
            play = 0
            return play

if play == 1:
    play = run(1)

# finish up and save
dumped = yaml.dump(player)

save_file_quit = save_file
with open(save_file_quit, "w") as f:
    f.write(dumped)
