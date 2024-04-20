from flask import Flask, render_template, session, request, redirect, url_for
from helper import apology, insertinfo, getinfo, login_required, delete_row, getinfov2, replacetinfo, updatecount
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from datetime import datetime
app = Flask(__name__, template_folder='templates')
app.secret_key = "hello"

current_datetime = datetime.now()


@app.route("/")
@login_required
def index():
    updatecount()
    decks = getinfo("name", "decks", "user_id", session["user_id"][0])
    return render_template('index.html', decks = decks)

db = sqlite3.connect('flashcard.db')
cursor = db.cursor()

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        passwd = request.form.get("password")
        usern = request.form.get("username")
        users = getinfo("username","users","username",usern)
        if not usern:
            return apology("Must provide username")
        elif not passwd:
            return apology("Must provide passwd")
        elif len(users) !=1:
            return apology("user dont exits")
        else:
            hash = getinfo("hash", "users", "username", usern)
            if not check_password_hash(hash[0], passwd):
                return apology("password incorect")
            else:
                session["user_id"] = getinfo("id", "users", "username", usern)
                session["username"] = users[0] 
    return redirect("/")

@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        usern = request.form.get("username")
        passwd = request.form.get("password")
        confi = request.form.get("confirmation")
        users = getinfo("username", "users")
        if not usern:
            return apology("Must provide username")
        elif not passwd:
            return apology("Must provide passwd")
        elif not confi:
            return apology("Password incorrect")
        elif usern in users:
            return apology("username is already taken")
        else:
            insertinfo("users", username = usern, hash = generate_password_hash(passwd))
    return redirect("/login")    

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/open", methods = ["POST"])
@login_required
def open():
    name = request.form.get("open")
    deck_id = getinfo("id", "decks", "name", name)[0]
    card_ids = getinfov2("id", "cards", deck_id = deck_id, count = 0)
    if len(card_ids) == 0:
        return render_template("deck.html", deck_id = deck_id, deckname = name, box_id = 0)
    box_idr = getinfov2("box_id", "cards", id = card_ids[0])[0]
    return render_template("deck.html", deck_id = deck_id, deckname = name, box_id = box_idr)

@app.route("/delete", methods = ["POST"])
@login_required
def delete():
    deck_name = request.form.get("delete")
    delete_row("decks", "name", deck_name)
    return redirect("/")

@app.route("/add", methods = ["POST"])
@login_required
def add():
    deck_name = request.form.get("deck_name")
    user_id = int(getinfo("id", "users", "username", session["username"])[0])
    if not deck_name:
        return apology("must provide deckname")
    else:
        insertinfo("decks", user_id = user_id, name = deck_name)
    return redirect("/")

@app.route("/addcardpage", methods = ["POST"])
@login_required
def addcardpage():
    deck_id = int(request.form.get("deck_id"))
    deckname = getinfo("name", "decks", "id", deck_id)[0]
    return render_template("addcard.html", deck_id = deck_id, deckname = deckname)

@app.route("/addcard", methods = ["POST"])
@login_required
def addcard():
    front = request.form.get("front")
    back = request.form.get("back")
    box_id = 1
    deck_id = int(request.form.get("deck_id"))
    deckname = getinfo("name", "decks", "id", deck_id)[0]
    insertinfo("cards", front = front, back = back, box_id = box_id, deck_id = deck_id, count = 0, last_update_time = current_datetime)
    return render_template("addcard.html", deck_id = deck_id, deckname = deckname)

@app.route("/openbox", methods = ["POST", "GET"])
@login_required
def openbox():
    box_id = request.form.get("box_id")
    deck_id = request.form.get("deck_id")
    deckname = getinfov2("name", "decks", id = deck_id)[0]
    fronts1 = getinfov2("front", "cards", box_id = box_id, deck_id = deck_id)
    fronts = []
    for front in fronts1:
        fronts.append(front[:70])
    card_ids = getinfov2("id", "cards", deck_id = deck_id, box_id = box_id)
    return render_template("insidebox.html", fronts = fronts, deckname = deckname, card_ids = card_ids, box_id = box_id, deck_id = deck_id)

@app.route("/deletecard", methods = ["POST"])
@login_required
def deletecard():
    card_id = request.form.get("card_id")
    delete_row("cards", "id", card_id)
    box_id = request.form.get("box_id")
    deck_id = request.form.get("deck_id")
    deckname = getinfov2("name", "decks", id = deck_id)[0]
    fronts1 = getinfov2("front", "cards", box_id = box_id, deck_id = deck_id)
    fronts = []
    for front in fronts1:
        fronts.append(front[:70])
    card_ids = getinfov2("id", "cards", deck_id = deck_id, box_id = box_id)
    return render_template("insidebox.html", fronts = fronts, deckname = deckname, card_ids = card_ids, box_id = box_id, deck_id = deck_id)

@app.route("/editpage", methods = ["POST"])
@login_required
def editpage():
    card_id = request.form.get("card_id")
    deckname = getinfov2("name", "decks", id = getinfov2("deck_id", "cards", id = card_id)[0])[0]
    front = getinfov2("front", "cards", id = card_id)[0]
    back = getinfov2("back", "cards", id = card_id)[0]
    deck_id = getinfov2("deck_id", "cards", id = card_id)[0]
    box_id = getinfov2("box_id", "cards", id = card_id)[0]
    return render_template("edit.html", card_id = card_id, deckname = deckname, front = front, back = back, deck_id = deck_id, box_id = box_id)

@app.route("/edit", methods = ["POST"])
@login_required
def edit():
    card_id = request.form.get("card_id")
    deck_id = getinfov2("deck_id", "cards", id = card_id)[0]
    box_id = getinfov2("box_id", "cards", id = card_id)[0]
    deckname = getinfov2("name", "decks", id = deck_id)[0]
    front1 = request.form.get("front")
    front = front1[:70]
    back = request.form.get("back")
    count = getinfov2("count","cards", id = card_id)[0]
    replacetinfo("cards", front = front, back = back, id = card_id, deck_id = deck_id, box_id = box_id, count = count, last_update_time = current_datetime )
    back = getinfov2("back", "cards", id = card_id)[0]
    return render_template("edit.html", card_id = card_id, deckname = deckname, front = front, back = back, deck_id = deck_id, box_id = box_id)


@app.route("/learn", methods = ["POST"])
@login_required
def learn():
    deck_id = request.form.get("deck_id")
    box_id = int(request.form.get("box_id"))
    deckname = getinfov2("name", "decks", id  = deck_id)[0]
    
    if box_id == 0:
        return apology("you have no cards to learn")
    
    card_ids = getinfov2("id", "cards", deck_id = deck_id, count = 0)
    i = len(card_ids) - 1
    back = getinfov2("back", "cards", id = card_ids[i])[0]
    front = getinfov2("front", "cards", id = card_ids[i])[0]
    
    return render_template("learn.html", deck_id = deck_id, back = back, front = front, deckname = deckname, box_id = box_id)


@app.route("/learn2", methods = ["POST"])
@login_required
def learn2():
    deck_id = request.form.get("deck_id")
    box_id = int(request.form.get("box_id"))
    deckname = getinfov2("name", "decks", id  = deck_id)[0]
    card_idsr = getinfov2("id", "cards", deck_id = deck_id, count = 0)

    i = len(card_idsr) - 1

    backr = getinfov2("back", "cards", id = card_idsr[i])[0]
    frontr = getinfov2("front", "cards", id = card_idsr[i])[0]
    count = 0
    if box_id < 5:
        if box_id == 1:
            count = 0
        elif box_id == 2:
            count = 1
        elif box_id == 3:
            count = 3
        elif box_id == 4:
            count = 7
        replacetinfo("cards", id = card_idsr[i], back = backr, front = frontr, box_id = box_id, deck_id = deck_id, count = count, last_update_time = current_datetime)
    else:
        replacetinfo("cards", id = card_idsr[i], back = backr, front = frontr, box_id = 5, deck_id = deck_id, count = 14, last_update_time = current_datetime)  
    
    card_ids = getinfov2("id", "cards", deck_id = deck_id, count = 0)

    a = len(card_ids) - 1

    if len(card_ids) == 0:
        return render_template("congra.html")

    back = getinfov2("back", "cards", id = card_ids[a])[0]
    front = getinfov2("front", "cards", id = card_ids[a])[0]
    box_idr = getinfov2("box_id", "cards", id = card_ids[a])[0]
    
    return render_template("learn.html", deck_id = deck_id, back = back, front = front, deckname = deckname, box_id = box_idr)





if __name__ == '__main__':
    app.run(debug=True) 

