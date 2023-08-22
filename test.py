import os, sys

# stats
max_health = 100
current_health = 100

# display
bars = 20
remaining_health_symbol = "█"
lost_health_symbol = "_"

# colors
color_green = "\033[92m"
color_yellow = "\33[33m"
color_red = "\033[91m"
color_blue = "\33[34m"
color_default = "\033[0m"
health_color = color_green

while True:
    # bar update
    remaining_health_bars = round(current_health / max_health * bars)
    lost_health_bars = bars - remaining_health_bars

    # printing stats
    sys.stdout.write(f"HEALTH: {current_health} / {max_health}\n")
    sys.stdout.write(f"|{health_color}{remaining_health_bars * remaining_health_symbol}{lost_health_bars * lost_health_symbol}{color_default}|")
    sys.stdout.flush()

    # stat update
    current_health -= 1

    current_health = max(current_health, 0)

    # health color update
    if current_health > 0.66 * max_health:
        health_color = color_green
    elif current_health > 0.33 * max_health:
        health_color = color_yellow
    else:
        health_color = color_red

    # input
    input()
