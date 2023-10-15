from flask import Flask, render_template, url_for, request, redirect
import json
import os

food_containing_allergy = []
safeitems = []
unsafeitems = []

dir = os.listdir("restaurant_menu")
for i in range(len(dir)):
    dir[i] = dir[i].replace(".json", "")
    dir[i] = dir[i].replace("_", " ")



app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def home():
    global restaurant
    if request.method == "POST":
        rest = request.form['restsearch'].lower()
        restaurant = rest
        if rest in dir:
            return redirect(url_for("store"))
        else:
            return redirect(url_for("user", rest=rest))
    else:
        return render_template("basic.html")

@app.route("/restaurant", methods=['POST','GET'])
def store():
    global allergy
    if request.method == "POST":
        allergy = request.form['allsearch'].lower().split(", ")
        check_allergy(restaurant, allergy)
    return render_template("redirect.html", restaurant=restaurant.title(), food_containing_allergy=food_containing_allergy, safeitems=safeitems, unsafetimes=unsafeitems)

@app.route("/<rest>")
def user(rest):
    return f"<h1>We do not have {rest} as a restaurant.</hr>"

def check_allergy(restaurnat, allergy):
    global food_containing_allergy
    global safeitems, unsafeitems
    file = open(f"restaurant_menu/{restaurnat.replace(' ', '_')}.json", "r")
    dict = json.load(file)
    file.close()


    for menu_item in dict["menu"]:
        print(f"Menu item: {menu_item}")
        for ingredient in dict["menu"][menu_item]['ingredients']:
            print(f"Ingredient: {ingredient}")
            if ingredient.lower() in allergy and menu_item not in food_containing_allergy:
                food_containing_allergy.append(menu_item)
        if menu_item not in food_containing_allergy:
            safeitems.append([menu_item, dict["menu"][menu_item]["description"], str(dict["menu"][menu_item]["price"])])
        else:
            unsafeitems.append([menu_item, dict["menu"][menu_item]["description"], str(dict["menu"][menu_item]["price"])])

    print(safeitems)
    print(unsafeitems)



if __name__ == "__main__":
    app.run(debug=True)