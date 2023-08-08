import random
import yaml
import pickle
import battle

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
    save_name = input("Please name your save (make sure you add .yaml to the end): ")
    player = start_player
    dumped = yaml.dump(player)
    with open(save_name, "w") as f:
        f.write(dumped)
    save_file = save_name
    play = 1
elif create_save.lower().startswith('o'):
    open_save = input("Please choose a save to open (inclue .yaml ending): ")
    save_file = open_save
    with open(open_save) as f:    
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
        elif map["coordinate count"] > i:
            break

# gameplay here:
def run():
    print("Reserved keys:")
    print("N: Go north")
    print("S: Go south")
    print("E: Go east")
    print("W: Go west")
    print("I: view items. When in this view, type the name of an item to examine it.")
    print("Some items have special triggers, wich will often be stated in the description. Others can only be activated in certain situations, like in combat.")
    # Mapping stuff
    search(player["x"], player["y"])
    if map["point" + str(map_loaction)]["enemy"] > 0 and map_loaction not in player["defeated enemies"]:
        enemies_remaining = map["point" + str(map_loaction)]["enemy"]
        while enemies_remaining > 0:
            battle.fight()
            enemies_remaining -= 1
        if player["health"] > 0:
            player["defeated enemies"].append(map_loaction)
        else:
            die()

if play == 1:
    run()

# finish up and save
dumped = yaml.dump(player)

with open(save_file, "w") as f:
    f.write(dumped)