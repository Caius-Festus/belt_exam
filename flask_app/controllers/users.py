from flask import render_template, request, redirect, session
from flask_app import app, Bcrypt, flash
from flask_app.models.user import User
from flask_app.models.magazine import Magazine

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    session['check'] = 'register'
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "confirm_password" : request.form["confirm_password"]
    }
    if not User.validate_registration(data):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['password'] = pw_hash
    user_id = User.add_user(data)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    session['email'] = data['email']
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    session['check'] = 'login'
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not User.validate_login(data):
        return redirect("/")
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db["password"], request.form["password"]):
        flash("Wrong Password")
        return redirect("/")
    session['user_id'] = user_in_db['id']
    session['first_name'] = user_in_db['first_name']
    session['last_name'] = user_in_db['last_name']
    session['email'] = user_in_db['email']
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/user/account")
def profile():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "user_id" : session["user_id"]
    }
    created_mags = Magazine.get_magazines_created_by(data)
    subbed_mags = Magazine.get_subbed_mags_by(data)
    return render_template("user_account.html", created_mags=created_mags, subbed_mags=subbed_mags)

@app.route("/update_user", methods=["POST"])
def update_user():
    if "user_id" not in session:
        return redirect("/")
    if not User.validate_update(request.form):
        return redirect("/user/account")
    User.update_user(request.form)
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    return redirect("/user/account")
