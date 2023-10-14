from flask import Flask, render_template, url_for, request, redirect
import json

global allergy, restaurant


app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def home():
    global restaurant
    if request.method == "POST":
        rest = request.form['restsearch'].lower()
        restaurant = rest
        if rest=="taste of italy":
            return redirect(url_for("italy"))
        else:
            return redirect(url_for("user", rest=rest))
    else:
        return render_template("basic.html")

@app.route("/tasteofitaly", methods=['POST','GET'])
def italy():
    global allergy
    if request.method == "POST":
        allergy = request.form['allsearch'].lower()
        check_allergy(restaurant, allergy)
    return render_template("italy.html")

@app.route("/<rest>")
def user(rest):
    return f"<h1>We do not have {rest} as a restaurant.</hr>"

def check_allergy(restaurnat, allergy):
    food_containing_allergy = []
    file = open(f"restaurant_menu/{restaurnat.replace(' ', '_')}.json", "r")
    menu = json.load(file)
    file.close()

    for menu_item in menu:
        for ingredient in menu[menu_item]:
            if ingredient.lower() == allergy:
                food_containing_allergy.append(menu_item)

    print(f"Food containing allergy: {food_containing_allergy}")

if __name__ == "__main__":
    app.run(debug=True)