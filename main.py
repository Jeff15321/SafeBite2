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
    global allergy, unsafeitems, safeitems
    if unsafeitems != [] or safeitems != []:
        unsafeitems = []
        safeitems = []
    if request.method == "GET":
        file = open(f"restaurant_menu/{restaurant.replace(' ', '_')}.json", "r")
        dict = json.load(file)
        file.close()
        for menu_item in dict["menu"]:
            safeitems.append([menu_item, dict["menu"][menu_item]["description"], "$" + str(dict["menu"][menu_item]["price"])])
    elif request.method == "POST":
        allergy = request.form['allsearch'].lower().split(", ")
        check_allergy(restaurant, allergy)

    safecount = len(safeitems)
    totalcount = len(safeitems) + len(unsafeitems)
    if totalcount != 0:
        safepercent = safecount / totalcount
    else:
        safepercent = 0
    if len(safeitems) != 0:
        safetrue = True
    else:
        safetrue = False
    if len(unsafeitems) != 0:
        unsafetrue = True
    else:
        unsafetrue = False
    return render_template("redirect.html",
                           safetrue=safetrue,
                           unsafetrue=unsafetrue,
                           restaurant=restaurant.title(),
                           safepercent=safepercent,
                           food_containing_allergy=food_containing_allergy,
                           safeitems=safeitems,
                           unsafeitems=unsafeitems)

@app.route("/<rest>")
def user(rest):
    return f"<h1>We do not have {rest} as a restaurant.</hr>"

def check_allergy(restaurnat, allergy):

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
            safeitems.append([menu_item, dict["menu"][menu_item]["description"], "$" + str(dict["menu"][menu_item]["price"])])
        else:
            unsafeitems.append([menu_item, dict["menu"][menu_item]["description"], "$" + str(dict["menu"][menu_item]["price"])])
    food_containing_allergy.clear()
    print(safeitems)
    print(unsafeitems)


if __name__ == "__main__":
    app.run(debug=True)