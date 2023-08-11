import yaml
import random
from colors import *

# battle stats
enemy_max = random.randint(5, 21)
enemy_health = enemy_max
enemy_max_damage = random.randint(4, 8)
enemy_damage = 0
defend = 0
turn = True

#opens "save.yaml"
# with open("save.yaml") as f:
    # player = yaml.safe_load(f)

# if player["xp"] < 0:
#     player["xp"] = 0

def fight(player, item):
    # avoid circular imports
    # import stats
    global turn, enemy_health, defend, enemy_max, enemy_max_damage

    # while player still alive
    while player["health"] > 0:
        while turn:
            # Print HP stats and possible actions for the player
            print(COLOR_RED + "Enemy: " + enemy_health, COLOR_RESET_ALL +  "/", COLOR_GREEN + enemy_max, COLOR_BLUE + "; You: ", player["health"], COLOR_RESET_ALL + "/", COLOR_GREEN +  player["max health"] + COLOR_RESET_ALL)
            action = input("Attack, Defend, Use Item? ")
    
            if action.lower().startswith('a'):
                print(item[player["held item"]]["damage"])
                # attack formula
                enemy_health -= random.randint(0, int(item[player["held item"]]["damage"]))
                print("Enemy: ", enemy_health, "/", enemy_max)
                turn = False
            elif action.lower().startswith('d'):
                defend += random.randint(0, int(item[player["held item"]]["defend"]))
                # defend formula
                player["health"] += random.randint(0, 3)
                if player["health"] > player["max health"]:
                    player["health"] = player["max health"]
                turn = False
            elif action.lower().startswith('u'):
                item_input = input(player["inventory"])
                # use item
                if item in player["inventory"]:
                    if item_input == "Healing Potion":
                        # apply stats
                        player["health"] = player["max health"]
                        player["inventory"].remove('Healing Potion')
                        player["max health"] += 5
                        player["health"] = player["max health"]
                        turn = False
                    # hold weapon if it is one
                    if item_input in player["inventory"] and item[item_input]["type"] == "Weapon":
                        player["held item"] = "Axe"
                        print("You are now holding an Axe")
        while not turn:
            # if enemy is still alive
            if enemy_health > 0:
                damage = random.randint(0, enemy_max_damage) - defend
                defend = 0
                if damage > 0:
                    player["health"] -= damage
                print("The enemy dealt ", damage, " points of damage.")
                print("You have", player["health"], "health points.")
                turn = True
            else:
                player["xp"] += enemy_max * enemy_max_damage / 3
                player["health"] += random.randint(0, 3)
                # enemy_max = random.randint(5, 21)
                # enemy_health = enemy_max
                # enemy_max_damage = random.randint(4, 8)
                # defend = 0
                # turn = True
                still_playing = False
                return
    return



still_playing = True

# while still_playing:

#     fight()

#     still_playing = False

#     if player["health"] <= 0:
#         if player["cheat"] < 3:
#             cheatcode = input("What is the not-die code? ")
#             if cheatcode == "4":
#                 # cheat code was correct so keep playing
#                 player["cheat"] += 1
#                 player["health"] = 10
#                 still_playing = True
#             else:
#                 player["health"] = 10
#                 player["max health"] = 10
#                 player["x"] = 0
#                 player["y"] = 0
#                 player["inventory"] = ["Sword", "Healing Potion"]
#                 player["held item"] = "Sword"
#                 player["cheat"] = 0
#                 player["xp"] -= 100
                
#         else:
#             print("YOU DIED")
#             player["health"] = 10
#             player["max health"] = 10
#             player["x"] = 0
#             player["y"] = 0
#             player["inventory"] = ["Sword", "Healing Potion"]
#             player["held item"] = "Sword"
#             player["cheat"] = 0
#             player["xp"] -= 100

# put all the new data in the file
# dumped = yaml.dump(player)

# with open("save.yaml", "w") as f:
#     f.write(dumped)
