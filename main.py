import random
import yaml
import pickle
import battle
import os
import time
from colorama import Fore, Back, Style, deinit, init
from colors import *

# get start time
start_time = time.time()

# initialize colorama
init()

# says you are not playing.
play = 0

fought_enemy = False

separator = COLOR_STYLE_BRIGHT + "###############################" + COLOR_RESET_ALL

# opens data files
with open("map.yaml") as f:
    map = yaml.safe_load(f)

with open("items.yaml") as f:
    item = yaml.safe_load(f)

with open("enemies.yaml") as f:
    enemy = yaml.safe_load(f)

with open("start.yaml") as f:
    start_player = yaml.safe_load(f)

# first text you see

res = []

for search_for_saves in os.listdir():
    if search_for_saves.startswith("save_"):
        res.append(search_for_saves)

char1 = 'save_'
char2 = '.yaml'

for idx, ele in enumerate(res):
    res[idx] = ele.replace(char1, '')

for idx, ele in enumerate(res):
    res[idx] = ele.replace(char2, '')

print(COLOR_STYLE_BRIGHT + "Current saves: " + COLOR_RESET_ALL + COLOR_GREEN + str(res) + COLOR_RESET_ALL)

save_selection = input(COLOR_STYLE_BRIGHT + "Do you want to [o]pen saved game, create [n]ew game or [d]elete an existing save? " + COLOR_RESET_ALL)

if save_selection.lower().startswith('n'):
    enter_save_name = input("Please name your save: ")
    player = start_player
    dumped = yaml.dump(player)
    save_name = "save_" + enter_save_name + ".yaml"
    check_file = os.path.isfile(save_name)
    if check_file == True:
        print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Save file '" + save_name + "'" + " already exists" + COLOR_RESET_ALL)
        play = 0
        exit(1)
    with open(save_name, "w") as f:
        f.write(dumped)
    save_file = save_name
    play = 1
elif save_selection.lower().startswith('o'):
    open_save = input("Please choose a save to open: ")
    save_file = "save_" + open_save + ".yaml"
    check_file = os.path.isfile(save_file)
    if check_file == False:
        print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
        play = 0
        exit(1)
    with open(save_file) as f:
        player = yaml.safe_load(f)
    play = 1
elif save_selection.lower().startswith('q'):
    play = 0
    exit(1)
elif save_selection.lower().startswith('d'):
    delete_save = input("Please choose a save to delete: ")
    save_file = "save_" + delete_save + ".yaml"
    check_file = os.path.isfile(save_file)
    if check_file == False:
        print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: Couldn't find save file '" + save_file + "'" + COLOR_RESET_ALL)
        play = 0
        exit(1)
    with open(save_file) as f:
        verify = input("Are you sure you want to delete the following save (y/n)? ")
        if verify == "y":
            save_file = "save_" + delete_save + ".yaml"
            player = "placeholder, do not delete"
            os.remove(save_file)
            play = 0
        if verify == "n":
            player = "placeholder, do not delete"
            print("Aborting current process...")
            play = 0
    exit(1)
else:
    print(COLOR_RED + COLOR_STYLE_BRIGHT + "ERROR: That option is not allowed." + COLOR_RESET_ALL)
    play = 0
    exit(1)

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
        point_y = point_i["y"]
        if point_y == player["y"]:
            map_location_y = i
            return map_location_y

# gameplay here:
def run(play):
    print(separator)
    print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Reserved keys:" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "N: "+ COLOR_RESET_ALL + "Go north" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "S: "+ COLOR_RESET_ALL + "Go south" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "E: " + COLOR_RESET_ALL + "Go east" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "W: " + COLOR_RESET_ALL + "Go west" + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "D: " + COLOR_RESET_ALL + "Access to your diary.")
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "I: " + COLOR_RESET_ALL + "View items. When in this view, type the name of an item to examine it." + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "P: " + COLOR_RESET_ALL + "Choose which item to equip on you. When in this view, type the name of an item to equip it." + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "T: " + COLOR_RESET_ALL + "Throw an item. When in this view, type the name of an item to throw it away." + COLOR_RESET_ALL)
    print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Q: " + COLOR_RESET_ALL + "Quit game")
    print(" ")
    print(COLOR_GREEN + COLOR_STYLE_BRIGHT +"Hints:" + COLOR_RESET_ALL)
    print("If you find an item on the ground, type the name of the item to take it.")
    print("Some items have special triggers, which will often be stated in the description. Others can only be activated in certain situations, like in combat.")
    print(" ")
    # Mapping stuff

    while play == 1:
        global player

        # calculate player armor protection
        # and write it to the save file
        player_items = player["inventory"]
        player_items_number = len(player_items)
        count = 0
        global_armor_protection = 0
        p = True

        # loop to get player total armor protection
        while p:
            if count > ( player_items_number - 1 ):
                p = False
            if p == True:

                player_items_select = player_items[int(count)]

                if item[player_items_select]["type"] == "Armor Piece: Chestplate" and player["held chestplate"] == player_items_select:
                    item_armor_protection = item[player_items_select]["armor protection"]
                elif item[player_items_select]["type"] == "Armor Piece: Boots" and player["held boots"] == player_items_select:
                    item_armor_protection = item[player_items_select]["armor protection"]
                elif item[player_items_select]["type"] == "Armor Piece: Leggings" and player["held leggings"] == player_items_select:
                    item_armor_protection = item[player_items_select]["armor protection"]
                else:
                    item_armor_protection = 0

                global_armor_protection += item_armor_protection

                count += 1

        global_armor_protection = round(global_armor_protection, 2)

        player["armor protection"] = global_armor_protection

        # calculate player agility and
        # write it to the save file
        player_items = player["inventory"]
        player_items_number = len(player_items)
        count = 0
        global_agility = 0
        p = True

        # loop to get player total agility
        while p:
            if count > ( player_items_number - 1 ):
                p = False
            if p == True:

                player_items_select = player_items[int(count)]

                if item[player_items_select]["type"] == "Armor Piece: Chestplate" and player["held chestplate"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                elif item[player_items_select]["type"] == "Armor Piece: Boots" and player["held boots"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                elif item[player_items_select]["type"] == "Armor Piece: Leggings" and player["held leggings"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                elif item[player_items_select]["type"] == "Weapon" and player["held item"] == player_items_select:
                    item_agility = item[player_items_select]["agility"]
                else:
                    item_agility = 0

                global_agility += item_agility

                count += 1

        global_agility = round(global_agility, 2)
        player["agility"] = global_agility

        # calculate remaining inventory slots
        # and write it to the save files
        p2 = True
        count2 = 0
        global_inventory_slots = 0
        player_items = player["inventory"]
        player_items_number = len(player_items)

        # loop to get player total inventory slots
        while p2:
            if count2 > ( player_items_number - 1 ):
                p2 = False
            if p2 == True:

                player_items_select = player_items[int(count2)]

                if item[player_items_select]["type"] == "Bag":
                    item_invetory_slot = item[player_items_select]["inventory slots"]
                else:
                    item_invetory_slot = 0

                global_inventory_slots += item_invetory_slot

                count2 += 1

            player["inventory slots"] = global_inventory_slots

        # calculate remaining item slots

        player["inventory slots remaining"] = int(player["inventory slots"]) - int(player_items_number)

        map_location = search(player["x"], player["y"])
        map_location_x = search_specific_x()
        map_location_y = search_specific_y()
        map_zone = map["point" + str(map_location)]["map zone"]
        print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Coordinates:" + COLOR_RESET_ALL)
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "X: " + COLOR_RESET_ALL + str(map_location_x))
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Y: " + COLOR_RESET_ALL + str(map_location_y))
        print(COLOR_BLUE + COLOR_STYLE_BRIGHT + "Region: " + COLOR_RESET_ALL + str(map_zone))
        print(" ")
        print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "Possible actions:" + COLOR_RESET_ALL)
        if "North" not in map["point" + str(map_location)]["blocked"]:
            print("You can go North")
        if "South" not in map["point" + str(map_location)]["blocked"]:
            print("You can go South")
        if "East" not in map["point" + str(map_location)]["blocked"]:
            print("You can go East")
        if "West" not in map["point" + str(map_location)]["blocked"]:
            print("You can go West")
        if "None" not in map["point" + str(map_location)]["item"] and map_location not in player["taken items"]:
            take_item = input(COLOR_GREEN + "There are these items on the ground: " + COLOR_RESET_ALL + str(map["point" + str(map_location)]["item"]) + " ")
            if take_item in map["point" + str(map_location)]["item"]:
                if take_item in player["inventory"] and item[take_item]["type"] == "Utility":
                    print("You cannot take that item")
                elif player["inventory slots remaining"] == 0:
                    print("You cannot take that item, you don't have enough slots in your inventory")
                else:
                    player["inventory"].append(take_item)
                    player["taken items"].append(map_location)
        if map["point" + str(map_location)]["enemy"] > 0 and map_location not in player["defeated enemies"]:
            enemies_remaining = map["point" + str(map_location)]["enemy"]
            already_encountered = False
            while enemies_remaining > 0:
                battle.get_enemy_stats(player, item, enemy, map, map_location)
                if not already_encountered:
                    battle.encounter_text_show(player, item, enemy, map, map_location, enemies_remaining)
                    already_encountered = True
                battle.fight(player, item, enemy, map, map_location, enemies_remaining)
                enemies_remaining -= 1
            if round(random.uniform(.20, .50), 2) > .35:
                if map["point" + str(map_location)]["enemy_type"] == "generic":
                    list_enemies = ['Goblin', 'Orc', 'Orc Archer', 'Warg', "Cavern Troll"]
                if map["point" + str(map_location)]["enemy_type"] == "black":
                    list_enemies = ['Black Orc', 'Dark Marksman', 'Doomed Horror']

                choose_rand_enemy = random.randint(0, len(list_enemies) - 1)
                choose_rand_enemy = list_enemies[choose_rand_enemy]
                choosen_enemy = enemy[choose_rand_enemy]

                enemy_total_inventory = choosen_enemy["inventory"]

                enemy_items_number = len(enemy_total_inventory)
                choosen_item = enemy_total_inventory[random.randint(0, enemy_items_number - 1)]

                drop = input("Your enemy dropped a/an " + choosen_item + ". Do you want to grab it (y/n)?")
                if drop.lower().startswith('y'):
                    if choosen_item in player["inventory"] and item[choosen_item]["type"] == "Utility":
                        print("You cannot take that item")
                    elif player["inventory slots remaining"] == 0:
                        print("You cannot take that item, you don't have enough slots in your inventory")
                    else:
                        player["inventory"].append(choosen_item)
                        player["taken items"].append(map_location)
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
                    print(COLOR_GREEN + COLOR_STYLE_BRIGHT + "There are these items on the ground: ", map["point" + str(map_location)]["item"] + COLOR_RESET_ALL)
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
        elif command.lower().startswith('d'):
            print("Elapsed Days: " + COLOR_RED + str(round(player["elapsed time game days"], 1)) + COLOR_RESET_ALL)
            print("Known enemies:")
            enemies_list = str(player["enemies list"])
            enemies_list = enemies_list.replace("'None', ", '')
            which_enemy = input("You have these enemies in your diary: " + enemies_list + " ")
            print(" ")
            if which_enemy == "None":
                print("You don't know about that enemy.")
            elif which_enemy in player["enemies list"]:

                enemy_thumbnail = "imgs/" + which_enemy + ".txt"
                with open(enemy_thumbnail, 'r') as f:
                    print(f.read())

                print("Name: " + which_enemy)

                print("Plural: " + enemy[which_enemy]["plural"])
                enemy_average_damage = ( enemy[which_enemy]["damage"]["min damage"] + enemy[which_enemy]["damage"]["max damage"] ) / 2
                enemy_average_health = ( enemy[which_enemy]["health"]["min spawning health"] + enemy[which_enemy]["health"]["max spawning health"] ) / 2
                print("Average Damage: " + COLOR_RED + str(enemy_average_damage) + COLOR_RESET_ALL)
                print("Average Health: " + COLOR_RED + str(enemy_average_health) + COLOR_RESET_ALL)
                print("Agility: " + COLOR_RED + str(enemy[which_enemy]["agility"]) + COLOR_RESET_ALL)

                # drops
                enemy_drops = str(enemy[which_enemy]["inventory"])
                enemy_drops = enemy_drops.replace('[', '')
                enemy_drops = enemy_drops.replace(']', '')
                enemy_drops = enemy_drops.replace("'", '')
                print("Drops: " + str(enemy_drops))

                print("Description: " + enemy[which_enemy]["description"])
            else:
                print("You don't know about that enemy.")
            print(" ")
        elif command.lower().startswith('i'):
            print("Current Health: " + COLOR_RED + str(player["health"]) + COLOR_RESET_ALL)
            print("Maximum Health: " + COLOR_RED + str(player["max health"]) + COLOR_RESET_ALL)
            print("Armor Protection: " + COLOR_RED + str(player["armor protection"]) + COLOR_RESET_ALL)
            print("Agility: " + COLOR_RED + str(player["agility"]) + COLOR_RESET_ALL)
            print(" ")
            # inventory slots
            print("Inventory Slots: " + COLOR_RED + str(player["inventory slots"]) + COLOR_RESET_ALL)
            print("Inventory Slots Remaining: " + COLOR_RED + str(player["inventory slots remaining"]) + COLOR_RESET_ALL)
            print(" ")
            # equipment
            if player["held item"] == " ":
                print("You are currently holding no weapon")
            else:
                print("You are holding a/an " + COLOR_RED + player["held item"] + COLOR_RESET_ALL)
            if player["held chestplate"] == " ":
                print("You are currently wearing no chestplate")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held chestplate"] + COLOR_RESET_ALL)
            if player["held boots"] == " ":
                print("You are currently holding no boots")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held boots"] + COLOR_RESET_ALL)
            if player["held leggings"] == " ":
                print("You are currently holding no leggings")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held leggings"] + COLOR_RESET_ALL)
            print(" ")
            which_item = input("You have these items in your inventory: " + str(player["inventory"]) + " ")
            if which_item in player["inventory"]:
                print(" ")
                print("Name: " + which_item)
                print("Type: " + item[which_item]["type"])
                print("Description: " + item[which_item]["description"])
                if item[which_item]["type"] == "Armor Piece: Chestplate" or item[which_item]["type"] == "Armor Piece: Boots" or item[which_item]["type"] == "Armor Piece: Leggings":
                    print("             Armor pieces can protect you in fights, more the armor protection is higher, the more it protects you.")
                    print("Armor Protection: " + COLOR_RED + str(item[which_item]["armor protection"]) + COLOR_RESET_ALL)
                if item[which_item]["type"] == "Weapon":
                    print("Damage: " + COLOR_RED + str(item[which_item]["damage"]) + COLOR_RESET_ALL)
                    print("Defense: " + COLOR_RED + str(item[which_item]["defend"]) + COLOR_RESET_ALL)
                if item[which_item]["type"] == "Consumable":
                    print("Max Bonus: " + COLOR_RED + str(item[which_item]["max bonus"]) + COLOR_RESET_ALL)
                    print("Healing Level: " + COLOR_RED + str(item[which_item]["healing level"]) + COLOR_RESET_ALL)
                print(" ")
            else:
                print("You do not have that item.")
                print(" ")
        elif command.lower().startswith('t'):
            # equipment
            if player["held item"] == " ":
                print("You are currently holding no weapon")
            else:
                print("You are holding a/an " + COLOR_RED + player["held item"] + COLOR_RESET_ALL)
            if player["held chestplate"] == " ":
                print("You are currently holding no chestplate")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held chestplate"] + COLOR_RESET_ALL)
            if player["held boots"] == " ":
                print("You are currently holding no boots")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held boots"] + COLOR_RESET_ALL)
            if player["held leggings"] == " ":
                print("You are currently holding no leggings")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held leggings"] + COLOR_RESET_ALL)
            which_item = input("You have these items in your inventory: " + str(player["inventory"]) + " ")
            if which_item in player["inventory"]:
                ask = input("You won't be able to get this item back if your throw it away. Are you sure you want to throw away this item? (y/n) ")
                if ask.lower().startswith('y'):
                    if item[which_item]["type"] == "Bag":
                        if ( player["inventory slots remaining"] - item[which_item]["inventory slots"] ) < 0:
                            print("You cannot throw that item because it would cause your remaining inventory slots to be negative")
                            print(" ")
                    else:
                        player["inventory"].remove(which_item)
                        if which_item == player["held item"]:
                            player["held item"] = " "
                        if which_item == player["held chestplate"]:
                            player["held chestplate"] = " "
                        if which_item == player["held boots"]:
                            player["held boots"] = " "
                        if which_item == player["held leggings"]:
                            player["held leggings"] = " "
                    print(" ")
            else:
                print("You do not have that item.")
                print(" ")
        elif command.lower().startswith('p'):
            # equipment
            if player["held item"] == " ":
                print("You are currently holding no weapon")
            else:
                print("You are holding a/an " + COLOR_RED + player["held item"] + COLOR_RESET_ALL)
            if player["held chestplate"] == " ":
                print("You are currently holding no chestplate")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held chestplate"] + COLOR_RESET_ALL)
            if player["held boots"] == " ":
                print("You are currently holding no boots")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held boots"] + COLOR_RESET_ALL)
            if player["held leggings"] == " ":
                print("You are currently holding no leggings")
            else:
                print("You are wearing a/an " + COLOR_RED + player["held leggings"] + COLOR_RESET_ALL)
            which_item = input("You have these items in your inventory: " + str(player["inventory"]) + " ")
            if which_item in player["inventory"]:
                if item[which_item]["type"] == "Weapon":
                    player["held item"] = which_item
                    print("Equipped a/an " + which_item)
                elif item[which_item]["type"] == "Armor Piece: Chestplate":
                    player["held chestplate"] = which_item
                    print("Equipped a/an " + which_item)
                elif item[which_item]["type"] == "Armor Piece: Boots":
                    player["held boots"] = which_item
                    print("Equipped a/an " + which_item)
                elif item[which_item]["type"] == "Armor Piece: Leggings":
                    player["held leggings"] = which_item
                    print("Equipped a/an " + which_item)
                else:
                    print("You cannot equip a/an " + which_item)
                print(" ")
            else:
                print("You do not have that item.")
                print(" ")
        elif command.lower().startswith('m'):
            if "Map" in player["inventory"]:
                print("**|**")
                print("*[+]*")
                print("**⊥**")
                print(" ")
            else:
                print("You do not have a map.")
                print(" ")
        elif command in map["point" + str(map_location)]["item"]:
            if command not in player["inventory"]:
                player["inventory"].append(command)
            else:
                print("You already have that item.")
        elif command.lower().startswith('q'):
            print(separator)
            play = 0
            return play
        else:
            print("'" + command + "' is not a valid command")

if play == 1:
    play = run(1)

# calculate and convert elapsed time

# get end time
end_time = time.time()

# calculate elapsed time
elapsed_time = end_time - start_time
elapsed_time = round(elapsed_time, 2)

game_elapsed_time = 0.004167 * elapsed_time # 60 seconds irl = 0.25 days in-game
game_elapsed_time = round(game_elapsed_time, 2)

player["elapsed time seconds"] = elapsed_time + player["elapsed time seconds"]
player["elapsed time game days"] = game_elapsed_time + player["elapsed time game days"]

# finish up and save
dumped = yaml.dump(player)

save_file_quit = save_file
with open(save_file_quit, "w") as f:
    f.write(dumped)


# deinitialize colorame
deinit()

