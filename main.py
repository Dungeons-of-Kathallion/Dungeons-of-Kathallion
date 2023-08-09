import random
import yaml
import pickle
import battle
import os

# varibles
# room1x = random.randint

# says you are not playing.
play = 0

fought_enemy = False
# opens "save.yaml"
# with open("save.yaml") as f:
#     player = yaml.safe_load(f)

with open("items.yaml") as f:
    item = yaml.safe_load(f)

create_save = input("Do you want to [o]pen saved game or create [n]ew game? ")

if create_save.lower().startswith('n'):
    enter_save_name = input("Please name your save: ")
    player = {
        "health":10,
        "max health":10,
        "xp":0,
        "x":0,
        "y":0,
        "inventory":["Sword", "Healing Potion"],
        "held item":"Sword",
        "cheat":0
    }
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

# gameplay here:
while play == 1:
    print("Type 'q' to save and quit.")
    if player["x"] == 0 and player["y"] == 0:
        which_direction = input("You can go north, south, east or west.")
        if which_direction.lower().startswith('n'):
            player["y"] += 1
        elif which_direction.lower().startswith('s'):
            player["y"] -= 1
        elif which_direction.lower().startswith('e'):
            player["x"] += 1
        elif which_direction.lower().startswith('w'):
            player["x"] -= 1
        elif which_direction.lower().startswith('q'):
            play = 0
        else:
            print("ERROR: That option is not allowed.")

    elif player["x"] == 0 and player["y"] == 1:
        which_direction = input("You can go north, or south.")
        if which_direction.lower().startswith('n'):
            player["y"] += 1
        elif which_direction.lower().startswith('s'):
            player["y"] -= 1
        # elif which_direction.lower().startswith('e'):
        #     player["x"] += 1
        # elif which_direction.lower().startswith('w'):
        #     player["x"] -= 1
        elif which_direction.lower().startswith('q'):
            play = 0
        else:
            print("ERROR: That option is not allowed.")

    elif player["x"] == 0 and player["y"] == -1:
        which_direction = input("You can go north, east, or west.")
        if which_direction.lower().startswith('n'):
            player["y"] += 1
        # elif which_direction.lower().startswith('s'):
        #     player["y"] -= 1
        elif which_direction.lower().startswith('e'):
            player["x"] += 1
        elif which_direction.lower().startswith('w'):
            player["x"] -= 1
        elif which_direction.lower().startswith('q'):
            play = 0
        else:
            print("ERROR: That option is not allowed.")

    elif player["x"] == 1 and player["y"] == 0:
        which_direction = input(
            "You can go west. There is a map on the ground. (type T to take the map, press M to view it when you have it.)")
        # if which_direction.lower().startswith('n'):
        #     player["y"] += 1
        # elif which_direction.lower().startswith('s'):
        #     player["y"] -= 1
        # elif which_direction.lower().startswith('e'):
        #     player["x"] += 1
        if which_direction.lower().startswith('w'):
            player["x"] -= 1
        elif which_direction.lower().startswith('t'):
            if 'Map' not in player["inventory"]:
                player["inventory"].append('Map')
        elif which_direction.lower().startswith('m'):
            if 'Map' in player["inventory"]:
                print("**|**")
                print("*[+]*")
                print("**⊥**")
        elif which_direction.lower().startswith('q'):
            play = 0
        else:
            print("ERROR: That option is not allowed.")

    elif player["x"] == -1 and player["y"] == 0:
        which_direction = input(
            "You can go east. There is an axe on the ground. (type T to take the axe.)")
        # if which_direction.lower().startswith('n'):
        #     player["y"] += 1
        # elif which_direction.lower().startswith('s'):
        #     player["y"] -= 1
        if which_direction.lower().startswith('e'):
            player["x"] += 1
        # if which_direction.lower().startswith('w'):
        #     player["x"] -= 1
        elif which_direction.lower().startswith('t'):
            if 'Axe' not in player["inventory"]:
                player["inventory"].append('Axe')
        elif which_direction.lower().startswith('m'):
            if 'Map' in player["inventory"]:
                print("**|**")
                print("*[+]*")
                print("**⊥**")
        elif which_direction.lower().startswith('q'):
            play = 0

        else:
            print("ERROR: That option is not allowed.")

    # elif player["x"] == 0 and player["y"] == -1:
    #     which_direction = input(
    #         "You can go north, east, and west.")
    #     if which_direction.lower().startswith('n'):
    #         player["y"] += 1
    #     # elif which_direction.lower().startswith('s'):
    #     #     player["y"] -= 1
    #     if which_direction.lower().startswith('e'):
    #         player["x"] += 1
    #     if which_direction.lower().startswith('w'):
    #         player["x"] -= 1
    #     # elif which_direction.lower().startswith('t'):
    #     #     if 'Axe' not in player["inventory"]:
    #     #         player["inventory"].append('Axe')
    #     elif which_direction.lower().startswith('m'):
    #         if 'Map' in player["inventory"]:
    #             print("**|**")
    #             print("*[+]*")
    #             print("**⊥**")
    #     elif which_direction.lower().startswith('q'):
    #         play = 0
    #     else:
    #         print("ERROR: That option is not allowed.")

    elif player["x"] == -1 and player["y"] == -1:
        which_direction = input(
            "You can go west.")
        # if which_direction.lower().startswith('n'):
        #     player["y"] += 1
        # elif which_direction.lower().startswith('s'):
        #     player["y"] -= 1
        if which_direction.lower().startswith('e'):
            player["x"] += 1
        # if which_direction.lower().startswith('w'):
        #     player["x"] -= 1
        # elif which_direction.lower().startswith('t'):
        #     if 'Axe' not in player["inventory"]:
        #         player["inventory"].append('Axe')
        elif which_direction.lower().startswith('m'):
            if 'Map' in player["inventory"]:
                print("**|**")
                print("*[+]*")
                print("**⊥**")
        elif which_direction.lower().startswith('q'):
            play = 0
        else:
            print("ERROR: That option is not allowed.")

    elif player["x"] == 1 and player["y"] == -1:
        if fought_enemy == False:
            which_direction = input(
                "You can go west. There is an enemy here...preparing to fight!")
            battle.fight(player, item)
            fought_enemy = True
            # checks to see if you are dead.
            if player["health"] <= 0 and play == 1:
                if player["cheat"] < 3:
                    cheatcode = input("What is the not-die code?")
                    if not cheatcode == 43590:
                        player["health"] = 10
                        player["max health"] = 10
                        player["xp"] = 0
                        player["x"] = 0
                        player["y"] = 0
                        player["inventory"] = ["Sword", "Healing Potion"]
                        player["held item"] = "Sword"
                        player["cheat"] = 0
                        play = 0
                    else:
                        player["cheat"] += 1
                        player["health"] = player["max helth"]
                else:
                    print("YOU DIED")
                    player["health"] = 10
                    player["max health"] = 10
                    player["xp"] = 0
                    player["x"] = 0
                    player["y"] = 0
                    player["inventory"] = ["Sword", "Healing Potion"]
                    player["held item"] = "Sword"
                    player["cheat"] = 0
                    play = 0

        else:
            which_direction = input(
                "You can go west.")
            # if which_direction.lower().startswith('n'):
            #     player["y"] += 1
            # elif which_direction.lower().startswith('s'):
            #     player["y"] -= 1
            # if which_direction.lower().startswith('e'):
            #     player["x"] += 1
            if which_direction.lower().startswith('w'):
                player["x"] -= 1
            # elif which_direction.lower().startswith('t'):
            #     if 'Axe' not in player["inventory"]:
            #         player["inventory"].append('Axe')
            elif which_direction.lower().startswith('m'):
                if 'Map' in player["inventory"]:
                    print("**|**")
                    print("*[+]*")
                    print("**⊥**")
            elif which_direction.lower().startswith('q'):
                play = 0
            else:
                print("ERROR: That option is not allowed.")
    else:
        print("ERROR: You have traveled out of bounds.")
        print("Teleporting to start...")
        player["x"] = 0
        player["y"] = 0

# put all the new data in the file
dumped = yaml.dump(player)

save_file_quit = save_file
with open(save_file_quit, "w") as f:
    f.write(dumped)
