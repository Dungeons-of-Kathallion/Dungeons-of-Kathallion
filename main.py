import random
import yaml
import pickle
import battle
import os
from colorama import Fore, Back, Style, deinit, init

# initialize colorama
init()

# says you are not playing.
play = 0

fought_enemy = False

# import 'color palette'
# Basic colors
color_reset = Fore.RESET
color_black = Fore.BLACK
color_white = Fore.WHITE
color_red = Fore.RED
color_green = Fore.GREEN
color_yellow = Fore.YELLOW
color_blue = Fore.BLUE
color_magenta = Fore.MAGENTA
color_cyan = Fore.CYAN
# Background colors
color_back_reset = Back.RESET
color_back_black = Back.BLACK
color_back_white = Back.WHITE
color_back_red = Back.RED
color_back_green = Back.GREEN
color_back_yellow = Back.YELLOW
color_back_blue = Back.BLUE
color_back_magenta = Back.MAGENTA
color_back_cyan = Back.CYAN
# Text styles
color_style_normal = Style.NORMAL
color_style_dim = Style.DIM
color_style_bright = Style.BRIGHT

color_reset_all = Style.RESET_ALL

# opens data files
with open("map.yaml") as f:
    map = yaml.safe_load(f)

with open("items.yaml") as f:
    item = yaml.safe_load(f)

with open("start.yaml") as f:
    start_player = yaml.safe_load(f)

save_selection = input(color_style_bright + "Do you want to [o]pen saved game, create [n]ew game or [d]elete an existing save? " + color_reset_all)

if save_selection.lower().startswith('n'):
    enter_save_name = input("Please name your save: ")
    player = start_player
    dumped = yaml.dump(player)
    save_name = "save_" + enter_save_name + ".yaml"
    with open(save_name, "w") as f:
        f.write(dumped)
    save_file = save_name
    play = 1
elif save_selection.lower().startswith('o'):
    open_save = input("Please choose a save to open: ")
    save_file = "save_" + open_save + ".yaml"
    check_file = os.path.isfile(save_file)
    if check_file == False:
        print("ERROR: Couldn't find save file '" + save_file + "'")
        play = 0
        exit(1)
    with open(save_file) as f:    
        player = yaml.safe_load(f)
    play = 1
elif save_selection.lower().startswith('d'):
    delete_save = input("Please choose a save to delete: ")
    save_file = "save_" + delete_save + ".yaml"
    check_file = os.path.isfile(save_file)
    if check_file == False:
        print("ERROR: Couldn't find save file '" + save_file + "'")
        play = 0
        exit(1)
    with open(save_file) as f:
        verify = input("Are you sure you want to delete the following save (y/n)? ")
        if verify == "y":
            player = "placeholder, do not delete"
            os.remove(save_file)
            play = 0
        if verify == "n":
            player = "placeholder, do not delete"
            print("Aborting current process...")
            play = 0
else:
    print("ERROR: That option is not allowed.")

# funcion to search through the map file
def search(x, y):
    global map_location
    for i in range(0, map["coordinate count"]):
        point_i = map["point" + str(i)]
        point_x, point_y = point_i["x"], point_i["y"]
        # print(i, point_x, point_y, player)
        if point_x == player["x"] and point_y == player["y"]:
            map_location = i
            return map_location

def search_specific_x():
    global map_location_x
    for i in range(0, map["coordinate count"]):
        point_i = map["point" + str(i)]
        point_x = point_i["x"]
        if point_x == player["x"]:
            map_location_x = i
            return map_location_x

def search_specific_y():
    global map_location_y
    for i in range(0, map["coordinate count"]):
        point_i = map["point" + str(i)]
        point_y = point_i["x"]
        if point_y == player["y"]:
            map_location_y = i
            return map_location_y

# gameplay here:
def run(play):
    separator = "###############################"
    print(separator)
    print("Reserved keys:")
    print("N: Go north")
    print("S: Go south")
    print("E: Go east")
    print("W: Go west")
    print("I: View items. When in this view, type the name of an item to examine it.")
    print("Q: Quit game")
    print(" ")
    print("Hints:")
    print("If you find an item on the ground, type the name of the item to take it.")
    print("Some items have special triggers, wich will often be stated in the description. Others can only be activated in certain situations, like in combat.")
    print(" ")
    # Mapping stuff

    while play == 1:
        global player
        map_location = search(player["x"], player["y"])
        map_location_x = search_specific_x()
        map_location_y = search_specific_y()
        print("Coordinates:")
        print("X: " + str(map_location_x))
        print("Y: " + str(map_location_y))
        print(" ")
        if "North" not in map["point" + str(map_location)]["blocked"]:
            print("You can go North")
        if "South" not in map["point" + str(map_location)]["blocked"]:
            print("You can go South")
        if "East" not in map["point" + str(map_location)]["blocked"]:
            print("You can go East")
        if "West" not in map["point" + str(map_location)]["blocked"]:
            print("You can go West")
        if "None" not in map["point" + str(map_location)]["item"]:
            take_item = input("There are these items on the ground: " + str(map["point" + str(map_location)]["item"]))
            if take_item in map["point" + str(map_location)]["item"]:
                if take_item in player["inventory"]:
                    print("You already have that.")
                else:
                    player["inventory"].append(take_item)
        if map["point" + str(map_location)]["enemy"] > 0 and map_location not in player["defeated enemies"]:
            enemies_remaining = map["point" + str(map_location)]["enemy"]
            while enemies_remaining > 0:
                battle.fight(player, item)
                enemies_remaining -= 1
            if player["health"] > 0:
                player["defeated enemies"].append(map_location)
                if "North" not in map["point" + str(map_location)]["blocked"]:
                    print("You can go North")
                if "South" not in map["point" + str(map_location)]["blocked"]:
                    print("You can go South")
                if "East" not in map["point" + str(map_location)]["blocked"]:
                    print("You can go East")
                if "West" not in map["point" + str(map_location)]["blocked"]:
                    print("You can go West")
                if "None" not in map["point" + str(map_location)]["item"]:
                    print("There are these items on the ground: ", map["point" + str(map_location)]["item"])
            else:
                if player["cheat"] < 3:
                    cheatcode = input("What is the not-die code? ")
                    if cheatcode == "43590":
                        player["cheat"] += 1
                        player["health"] = player["max health"]
                    else:
                        player = start_player
                        play = 0
                        return play
                else:
                    print("You've cheated too much! No more lives!")
                    player = start_player
                    play = 0
                    return play
        print(" ")
        command = input("What will you do?\n")
        print(" ")
        if command.lower().startswith('go'):
            print("Rather than saying Go <direction>, simply say <direction>.")
        elif command.lower().startswith('n'):
            if "North" in map["point" + str(map_location)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["y"] += 1
        elif command.lower().startswith('s'):
            if "South" in map["point" + str(map_location)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["y"] -= 1
        elif command.lower().startswith('e'):
            if "East" in map["point" + str(map_location)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["x"] += 1
        elif command.lower().startswith('w'):
            if "West" in map["point" + str(map_location)]["blocked"]:
                print("You cannot go that way.")
            else:
                player["x"] -= 1
        elif command.lower().startswith('i'):
            which_item = input("You have these items in your inventory: " + str(player["inventory"]) + " ")
            if which_item in player["inventory"]:
                print(" ")
                print("Name: " + which_item)
                print("Type: " + item[which_item]["type"])
                print("Description: " + item[which_item]["description"])
                if item[which_item]["type"] == "Weapon":
                    print("Damage: " + str(item[which_item]["damage"]))
                    print("Defense: " + str(item[which_item]["defend"]))
                if item[which_item]["type"] == "Consumable":
                    print("Max Bonus: " + str(item[which_item]["max bonus"]))
                    print("Healing Level: " + str(item[which_item]["healing level"]))
                print(" ")
            else:
                print("You do not have that item.")
        elif command.lower().startswith('m'):
            if "Map" in player["inventory"]:
                print("**|**")
                print("*[+]*")
                print("**⊥**")
            else:
                print("You do not have a map.")
        elif command in map["point" + str(map_location)]["item"]:
            if command not in player["inventory"]:
                player["inventory"].append(command)
            else:
                print("You already have that item.")
        elif command.lower().startswith('q'):
            print(separator)
            play = 0
            return play

if play == 1:
    play = run(1)

# finish up and save
dumped = yaml.dump(player)

save_file_quit = save_file
with open(save_file_quit, "w") as f:
    f.write(dumped)

# deinitialize colorame
deinit()

