import json
import os
from main import *


directory = "restaurant_menu"
file = open("restaurant_menu/taste_of_italy.json", "r")
menu = json.load(file)
file.close()

food_containing_allergy = []

for menu_item in menu:
    for ingredient in menu[menu_item]:
        if ingredient.lower() == "eggs":
            food_containing_allergy.append(menu_item)

print(f"Food containing allergy: {food_containing_allergy}")






print(menu)
