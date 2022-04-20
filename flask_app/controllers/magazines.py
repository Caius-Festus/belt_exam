from flask import render_template, request, redirect, session, jsonify
from flask_app import app, Bcrypt, flash
from flask_app.models.magazine import Magazine


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    magazines = []
    mag_ids = Magazine.get_all_magazines()
    for row_in_db in mag_ids:
        magazines.append(Magazine.get_magazine(row_in_db))
    return render_template("dashboard.html", magazines=magazines)

@app.route("/new")
def new():
    if "user_id" not in session:
        return redirect("/")
    return render_template("new_magazine.html")

@app.route("/add_magazine", methods=["POST"])
def add_magazine():
    if "user_id" not in session:
        return redirect("/")
    if not Magazine.validate_magazine(request.form):
        return redirect("/new")
    Magazine.add_magazine(request.form)
    return redirect("/dashboard")

@app.route("/delete/<magazine_id>")
def delete_magazine(magazine_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : magazine_id
    }
    Magazine.delete_magazine(data)
    return redirect("/user/account")

@app.route("/show/<magazine_id>")
def show(magazine_id):
    data = {
        "id" : magazine_id
    }
    magazine = Magazine.get_full_magazine(data)
    return render_template("show_magazine.html", magazine=magazine)

@app.route("/subscribe/<user_id>/<magazine_id>")
def subscribe(user_id, magazine_id):
    data = {
        "user_id" : user_id,
        "magazine_id" : magazine_id
    }
    Magazine.subscribe(data)
    return redirect("/dashboard")

@app.route("/unsubscribe/<user_id>/<magazine_id>")
def unsubscribe(user_id, magazine_id):
    data = {
        "user_id" : user_id,
        "magazine_id" : magazine_id
    }
    Magazine.unsubscribe(data)
    return redirect("/dashboard")

# @app.route("/thoughts")
# def thoughts():
#     if "user_id" not in session:
#         return redirect("/")
#     thoughts = Thought.get_all_thoughts()
#     return render_template("thoughts.html", thoughts=thoughts)

# @app.route("/add_thought", methods=["POST"])
# def add_thought():
#     if not Thought.validate_thought(request.form):
#         return redirect("/thoughts")
#     Thought.add_thought(request.form)
#     return redirect("/thoughts")

# @app.route("/delete_thought/<thought_id>")
# def delete_thought(thought_id):
#     data = {
#         "id" : thought_id
#     }
#     Thought.delete_thought(data);
#     return redirect("/thoughts")

# @app.route("/like_interact", methods=["POST"])
# def like_interact():
#     data = request.form
#     print(data)
#     if data["like_action"] == "like":
#         Thought.add_user_likes_thought(data)
#     if data["like_action"] == "unlike":
#         Thought.remove_user_likes_thought(data)
#     return redirect("/thoughts")