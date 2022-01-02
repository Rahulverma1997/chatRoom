from flask import Blueprint, request, url_for, render_template, jsonify, redirect, flash
import jinja2
from flask_login import login_user, login_required, logout_user, current_user
from Room.modal import users1
from Room.db import save_user, get_user, update_user
from Room import login_manager
from Room.service import send_reset_email
from Room.token import get_reset_token, verify_reset_token
login_manager.login_view = 'auth_obj.login'

auth_obj = Blueprint("auth_obj", __name__, template_folder="templates")

@auth_obj.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        print('already loggd in')
        return redirect(url_for('hello'))

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = users1(firstname,lastname, email, password)
        new_user = new_user.create()
        save_user(new_user)
        flash('registeration successful')
        return render_template("register.html")

    return render_template("register.html")


@auth_obj.route("/login", methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        print('already loggd in')
        return redirect(url_for('hello'))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = get_user(email)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('hello', message1 = "login successful"))
        else:
            flash('login error')
            return render_template("login.html")

    return render_template("login.html")

@auth_obj.route("/logout")
@login_required
def logout():
    logout_user()
    print("already logged out")
    return redirect(url_for('hello', message = "logged out"))

@auth_obj.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))

    if request.method == "POST":
        email = request.form.get("email")
        user = get_user(email)
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('auth_obj.login'))
        else:
            flash('Email not found in database')
            return render_template('reset.html')
    return render_template('reset.html')

@auth_obj.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('hello')) 

    user = verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth_obj.reset_request'))

    if request.method == "POST":
        print("we are here")
        password = request.form.get("newpassword")
        update_user(user, password)
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth_obj.login'))
    
    return render_template('new_password.html', token = token)


@auth_obj.route("/varification/<token>", methods=['GET', 'POST'])
def varification_token(token):
    user = verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token, Please sign in and varify account', 'warning')
        return redirect(url_for('auth_obj.login'))

    if user:
        print("we are here")
        update_user(user, password)
        flash('Your account is varified now', 'success')
        return redirect(url_for('auth_obj.login'))
    
    return render_template('new_password.html', token = token)



@login_manager.user_loader
def load_user(email):
    return get_user(email)
    
    
