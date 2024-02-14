from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from ChatGPT_check_ingredient import ChatGPT_check_ingredient

import os
import sqlite3


app = Flask(__name__)

#used for login
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


conn = sqlite3.connect('restaurants.db')

curr = conn.cursor()

#restaurant related sql
curr.execute("""CREATE TABLE IF NOT EXISTS restaurants (
id INTEGER,
name TEXT NOT NULL,
description TEXT,
location TEXT NOT NULL,
username TEXT NOT NULL,
hash TEXT NOT NULL,
PRIMARY KEY(id)
)""")

curr.execute("""CREATE TABLE IF NOT EXISTS dishes (
id INTEGER,
name TEXT NOT NULL,
description TEXT,
restaurant_id INTEGER NOT NULL,
price FLOAT NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
)
""")

curr.execute("""CREATE TABLE IF NOT EXISTS ingredients(
id INTEGER ,
name TEXT NOT NULL,
PRIMARY KEY(id)
)""")

curr.execute("""CREATE TABLE IF NOT EXISTS dish_ingredient(
ingredient_id INTEGER NOT NULL,
dish_id INTEGER NOT NULL,
FOREIGN KEY(ingredient_id) REFERENCES ingredients(id),
FOREIGN KEY(dish_id) REFERENCES dishes(id)
)
""")
conn.commit()

conn.close()

@app.route("/", methods=['POST', 'GET'])
def home():
    if "restaurant_id" not in session.keys():
        session["restaurant_id"] = None
    conn = sqlite3.connect('restaurants.db')

    curr = conn.cursor()

    curr.execute("SELECT name, location FROM restaurants")

    global restaurant_list

    restaurant_list = curr.fetchall()

    conn.close()
    if request.method == "POST":
        temp_restaurant = request.form.get("restaurant_search").rsplit(" - ", 1)
        global_restaurant = temp_restaurant[0]
        #add location after
        if any(temp_restaurant[0].lower() == restaurant[0].lower() for restaurant in restaurant_list) and any(temp_restaurant[1].lower() == restaurant[1].lower() for restaurant in restaurant_list):
            return redirect(url_for("store", global_restaurant=global_restaurant))
        else:
            error_message = global_restaurant + " is not found"
            return redirect(url_for("error", error_message=error_message))

    if request.method == "GET":
        return render_template("basic.html", restaurant_list=restaurant_list)

@app.route("/restaurant", methods=['POST', 'GET'])
def store():
    if "restaurant_id" not in session.keys():
        session["restaurant_id"] = None

    global allergy, unsafeitems, safeitems
    allergy = []
    unsafeitems = []
    safeitems = []
    conn = sqlite3.connect('restaurants.db')
    curr = conn.cursor()

    global_restaurant = request.args.get("global_restaurant")
    curr.execute("SELECT id, description FROM restaurants WHERE LOWER(name) = LOWER(?)", (global_restaurant,))
    temp = curr.fetchone()

    restaurant_description = None
    sql_restaurant_id = None

    if temp is not None:
        sql_restaurant_id = temp[0]

    if temp[1] != None:
        restaurant_description = str(temp[1])

    curr.execute("SELECT name, description, price, id FROM dishes WHERE restaurant_id = ?", (sql_restaurant_id,))
    sql_dish_name = curr.fetchall()

    for i in sql_dish_name:
        temp_list = [i[0], i[1], i[2], i[3]]

        if session["restaurant_id"] == sql_restaurant_id:
            curr.execute("SELECT ingredient_id FROM dish_ingredient WHERE dish_id = ?", (i[3],))
            ingredient_id_list = curr.fetchall()

            for i in range(len(ingredient_id_list)):
                curr.execute("SELECT name FROM ingredients WHERE id = ?", (ingredient_id_list[i][0],))

                temp_list.append(curr.fetchone())
        safeitems.append(temp_list)
    conn.close()

    if request.method == "POST":
        allergy = request.form.get('allergy_search').lower().split(", ")
        check_allergy(sql_restaurant_id)

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

    admintrue = False

    if session["restaurant_id"] == sql_restaurant_id:
        admintrue = True

    return render_template("redirect.html",
                           description=restaurant_description,
                           admintrue=admintrue,
                           safetrue=safetrue,
                           unsafetrue=unsafetrue,
                           restaurant=global_restaurant,
                           safepercent=safepercent,
                           safeitems=safeitems,
                           unsafeitems=unsafeitems)


@app.route("/error")
def error():
    error_message = request.args.get("error_message", "An error occurred")
    return render_template("error.html", error_message=error_message)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    conn = sqlite3.connect('restaurants.db')

    curr = conn.cursor()

    if request.method == "POST":
        restaurant_id = session["restaurant_id"]
        curr.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,))

        old_password = curr.fetchone()[5]
        if (
            not request.form.get("old_password")
            or not request.form.get("new_password")
            or not request.form.get("confirmation")
        ):
            return render_template("error.html", error_message="Missing input")

        if request.form.get("new_password") != request.form.get("confirmation"):
            return render_template("error.html", error_message="Retyped password incorrect")

        if not check_password_hash(old_password, request.form.get("old_password")):
            return render_template("error.html", error_message="Old password incorrect")

        new_password = generate_password_hash(
            request.form.get("new_password"), method="pbkdf2", salt_length=16
        )
        curr.execute("UPDATE restaurants SET hash = ? WHERE id = ?", (new_password, restaurant_id))
        conn.commit()
        return redirect("/")
    elif request.method == "GET":
        return render_template("change_password.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        conn = sqlite3.connect('restaurants.db')

        curr = conn.cursor()
        if not request.form.get("username"):
            return render_template("error.html", error_message="Username must be completed")

        elif not request.form.get("password"):
            return render_template("error.html", error_message="Password must be completed")

        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", error_message="Confirmation not matched with password")

        elif not request.form.get("country") or not request.form.get("password") or not request.form.get("password"):
            return render_template("error.html", error_message="Location must be completed")

        elif not request.form.get("restaurant_name"):
            return render_template("error.html", error_message="Restaurant name must be completed")

        username = request.form.get("username")

        curr.execute(
            "SELECT * FROM restaurants WHERE username = ?", (username,)
        )
        rows = curr.fetchall()

        if len(rows) != 0:
            return render_template("error.html", error_message="Username already registered")

        hashed_password = generate_password_hash(
            request.form.get("password"), method="pbkdf2", salt_length=16
        )

        location = request.form.get("country") + ", " + request.form.get("city") + ", " + request.form.get("street")

        curr.execute(
            "INSERT INTO restaurants (name, description, location, username, hash) VALUES(?, ?, ?, ?, ?)", (request.form.get("restaurant_name"), request.form.get("description"), location, username, hashed_password)
        )
        conn.commit()
        conn.close()
        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=['POST', 'GET'])
def login():

    conn = sqlite3.connect('restaurants.db')

    curr = conn.cursor()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", error_message="Username must be completed")
        elif not request.form.get("password"):
            return render_template("error.html", error_message="Password must be completed")

        curr.execute(
            "SELECT * FROM restaurants WHERE username = ?", (request.form.get("username"),)
        )
        rows = curr.fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][5], request.form.get("password")
        ):
            return render_template("error.html", error_message="Invalid username or password")

        # Remember which user has logged in
        session["restaurant_id"] = rows[0][0]

        conn.close()

        return redirect("/admin")

    else:
        conn.close()

        return render_template("login.html")

@app.route("/admin", methods=['POST', 'GET'])
@login_required
def admin():
    if request.method == "POST":
        dish_name = request.form.get("dish-name")

        temp_ingredient = request.form.get("ingredient_str")

        description = request.form.get("description")

        if dish_name == None:
            return redirect(url_for("error", restaurant="Dish name must be inserted"))

        ingredient_list = temp_ingredient.split(",")

        for i in range(len(ingredient_list)):
            ingredient_list[i] = ingredient_list[i].lower()

        conn = sqlite3.connect('restaurants.db')

        curr = conn.cursor()
        if "remove_dish" in request.form:
            curr.execute(
                "SELECT name FROM dishes WHERE LOWER(name) = LOWER(?) AND restaurant_id = ?",(dish_name, session["restaurant_id"])
            )

            sql_dish_name = curr.fetchone()
            if sql_dish_name != None:
                sql_dish_name = sql_dish_name[0]

            if not sql_dish_name:
                return render_template("error.html", error_message="Dish not Found")

            curr.execute(
                "SELECT DISTINCT id FROM dishes WHERE LOWER(name) = LOWER(?) AND restaurant_id = ?",(dish_name, session["restaurant_id"])
            )

            sql_dish_id = curr.fetchone()
            if sql_dish_id != None:
                sql_dish_id = int(sql_dish_id[0])

            curr.execute("DELETE FROM dish_ingredient WHERE dish_id = ?", (sql_dish_id,))
            conn.commit()
            curr.execute("DELETE FROM dishes WHERE id = ?", (sql_dish_id,))
            conn.commit()
        elif "submit_dish" in request.form:
            try:
                price = float(request.form.get("price"))
            except ValueError:
                return render_template("error.html", error_message="Please provide a number for price.")

            if description is None:
                return redirect(url_for("error", restaurant="Description must be inserted"))
            if price is None:
                return redirect(url_for("error", restaurant="Price must be inserted"))
            if temp_ingredient is None:
                return redirect(url_for("error", restaurant="Ingredients must be inserted"))

            curr.execute(
                "SELECT DISTINCT name FROM dishes WHERE LOWER(name) = LOWER(?) AND restaurant_id = ?", (dish_name, session["restaurant_id"])
            )

            sql_dish_name = curr.fetchone()
            if sql_dish_name is not None:
                sql_dish_name = sql_dish_name[0]

            if not sql_dish_name:
                curr.execute(
                    "INSERT INTO dishes(name, restaurant_id, price, description) VALUES(?, ?, ?, ?)",
                    (dish_name, session["restaurant_id"], price, description))
                conn.commit()
            else:
                curr.execute("UPDATE dishes SET name = ?,price = ?, description = ? WHERE LOWER(name) = LOWER(?)", (dish_name, price, description, dish_name))
                conn.commit()
            curr.execute(
                "SELECT DISTINCT id FROM dishes WHERE LOWER(name) = LOWER(?) AND restaurant_id = ?",
                (dish_name, session["restaurant_id"]))

            sql_dish_id = curr.fetchone()

            if sql_dish_id != None:
                sql_dish_id = sql_dish_id[0]

            curr.execute("DELETE FROM dish_ingredient WHERE dish_id = ?", (sql_dish_id,))
            conn.commit()

            for i in (ingredient_list):

                curr.execute("SELECT DISTINCT id FROM ingredients WHERE LOWER(name) = LOWER(?)", (i,))

                sql_ingredient_id = curr.fetchone()
                if sql_ingredient_id != None:
                    sql_ingredient_id = sql_ingredient_id[0]

                if not sql_ingredient_id:
                    curr.execute("INSERT INTO ingredients(name) VALUES(?)", (i,))
                    conn.commit()

                curr.execute("SELECT DISTINCT id FROM ingredients WHERE LOWER(name) = LOWER(?)", (i,))

                sql_ingredient_id = curr.fetchone()

                # Update sql_ingredient_id
                if sql_ingredient_id != None:
                    sql_ingredient_id = sql_ingredient_id[0]

                curr.execute("SELECT COUNT(*) FROM dish_ingredient WHERE dish_id = ? AND ingredient_id = ?",
                             (sql_dish_id, sql_ingredient_id))

                sql_count_dish = curr.fetchone()[0]

                if sql_count_dish == 0 and sql_dish_id is not None and sql_ingredient_id is not None:
                    curr.execute("INSERT INTO dish_ingredient(dish_id, ingredient_id) VALUES(?, ?)",
                                 (sql_dish_id, sql_ingredient_id))
                    conn.commit()
        else:
            return render_template("error.html", error_message="Didn't work")

        curr.close()

        return render_template("admin.html")
    else:

        return render_template("admin.html")

def check_allergy(restaurant_id):

    global allergy, safeitems, unsafeitems

    temp_safeitems = []

    conn = sqlite3.connect('restaurants.db')

    curr = conn.cursor()

    ingredient_list = []

    for dish in safeitems:
        curr.execute("SELECT ingredient_id FROM dish_ingredient WHERE dish_id = ?", (dish[3],))
        #ISSUE: this is only giving me one and i don't know why
        #SOLUTION: curr.execute("SELECT name FROM ingredients WHERE id = (SELECT ingredient_id FROM dish_ingredient WHERE dish_id = ?)", (dish[3],))
        # Will not work because the second SELECT returns a tuple of tuple, you need to process the data first before you put it into the other sql query
        ingredient_id_list = curr.fetchall()

        dish_ingredient_list = []

        for i in range(len(ingredient_id_list)):
            curr.execute("SELECT name FROM ingredients WHERE id = ?", (ingredient_id_list[i][0],))

            dish_ingredient_list.append(curr.fetchone()[0])
        ingredient_list.append(dish_ingredient_list)

    ChatGPT_temp_list = [[], []]
    ChatGPT_temp_list[1] = ingredient_list
    ChatGPT_temp_list[0] = allergy

    output = ChatGPT_check_ingredient(ChatGPT_temp_list).strip()
    #sample output: [0, 1, 6, 9]

    if output.strip() != "[]":
        output = output[1:-1]

        output = [int(i) for i in output.split(",")]
    else:
        output = []

    for i in range(len(safeitems)):
        if i not in output:
            temp_safeitems.append(safeitems[i])
        else:
            unsafeitems.append(safeitems[i])


    safeitems = temp_safeitems
    conn.close()
if __name__ == "__main__":
    app.run(debug=True)
