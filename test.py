import json
import os

directory = "restaurant_menu"
file = open("restaurant_menu/taste_of_italy.json", "r")
menu = json.load(file)
file.close()

for menu_item in menu:
    print(f"Menu Item: {menu_item}")
    for ingredient_list in menu[menu_item]:
        print(f"Ingredients: {ingredient_list}")
    break



print(menu)
