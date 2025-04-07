import re
import secrets
import sqlite3

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe

import items
import users

app = Flask(__name__)
app.secret_key = "1234"

category = items.get_category_list()
condition = items.get_condition_list()

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index_get():
    all_items = items.get_items()
    return render_template("index.html", items=all_items, category=category, condition=condition)

@app.route("/user/<int:user_id>")
def user_get(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=user_items, category=category, condition=condition)

@app.route("/find_item")
def find_item_get():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results, category=category, condition=condition)

@app.route("/item/<int:item_id>")
def item_get(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    comments = items.get_comments(item_id)
    return render_template("show_item.html", item=item, comments=comments)

@app.route("/image/<int:item_id>")
def image_get(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    response = make_response(bytes(item["image"]))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/add_item")
def add_item_get():
    require_login()
    return render_template("add_item.html", category=category, condition=condition)

@app.route("/add_item", methods=["POST"])
def add_item_post():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)

    desc = request.form["desc"]
    if not desc or len(desc) > 1000:
        abort(403)

    price = request.form["price"]
    if not re.search("^[1-9][0-9]{0,3}$", price):
        abort(403)

    file = request.files["image"]
    if not file or not file.mimetype == "image/png":
        abort(403)

    image = file.read()
    if len(image) > 100 * 1024:
        abort(403)

    category1 = request.form["category"]
    if not category1 or not category1 in category:
        abort(403)

    condition1 = request.form["condition"]
    if not condition1 or not condition1 in condition:
        abort(403)

    user_id = session["user_id"]

    item_id = items.add_item(title, desc, price, image, category.index(category1), condition.index(condition1), user_id)

    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item_get(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_item.html", item=item, category=category, condition=condition)

@app.route("/edit_item", methods=["POST"])
def edit_item_post():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)

    desc = request.form["desc"]
    if not desc or len(desc) > 1000:
        abort(403)

    price = request.form["price"]
    if not re.search("^[1-9][0-9]{0,3}$", price):
        abort(403)

    file = request.files["image"]
    if file:
        if not file.mimetype == "image/png":
            abort(403)

        image = file.read()
        if len(image) > 100 * 1024:
            abort(403)
    else:
        image = item["image"]

    category1 = request.form["category"]
    if not category1 or not category1 in category:
        abort(403)

    condition1 = request.form["condition"]
    if not condition1 or not condition1 in condition:
        abort(403)
        
    items.update_item(item_id, title, desc, price, image, category.index(category1), condition.index(condition1))

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item_get(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/register")
def register_get():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: käyttäjänimi on jo varattu")
        return redirect("/register")

    return redirect("/")

@app.route("/login")
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/login")

@app.route("/logout")
def logout_get():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/comment", methods=["POST"])
def comment_post():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    comment = request.form["comment"]
    if not comment or len(comment) > 1000:
        abort(403)

    items.add_comment(item["user_id"], item_id, comment)

    return redirect("/item/" + str(item_id))