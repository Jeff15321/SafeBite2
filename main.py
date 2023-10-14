from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def home():
    if request.method == "POST":
        rest = request.form['restsearch'].lower()
        if rest=="taste of italy":
            return redirect(url_for("italy"))
        else:
            return redirect(url_for("user", rest=rest))
    else:
        return render_template("basic.html")

@app.route("/tasteofitaly", methods=['POST','GET'])
def italy():
    if request.method == "POST":
        allergy = request.form['allsearch'].lower()
    return render_template("italy.html")

@app.route("/<rest>")
def user(rest):
    return f"<h1>We do not have {rest} as a restaurant.</hr>"

if __name__ == "__main__":
    app.run(debug=True)