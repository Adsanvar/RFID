from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from . import bcrypt
import Dashboard.database as database
# from validate_email import validate_email
# from email.mime.text import MIMEText
# import os

# #sets up the authenticator blueprint
auth = Blueprint('auth', __name__)

# #route for the login
@auth.route('/login', methods=['POST'])
def login():
    #Adrian
    #if login button is activated proceed with authentication
    # usr = database.User(username="Admin", password = bcrypt.generate_password_hash("Admin").decode('utf-8'), firstname="Admin", lastname="Admin", role='Admin')
    # database.create_user(usr)    
    if 'login' in request.form:
        #checks to see if the the username field is empty
        if request.form.get('username'):
            #Non-empty
            name = request.form.get('username')
            pas = request.form.get('password')
            #obtaines user from database thru ORM
            usr = database.user_query(name)
            #checks if usr returned is null if so redirect to the login
            if usr == None:
                flash("Invalid Credentials", 'error')
                return redirect(url_for('home.login'))
            else:
                #authenticates user to db
                # Checks db.password hash with form password
                if usr.username == name and bcrypt.check_password_hash(usr.password, pas): 
                    login_user(usr)
                    return redirect(url_for('home.dashboard'))
                else:
                    flash("Invalid Credentials", 'error')
                    return redirect(url_for('home.login'))
        else:
            #empty
            flash("Please Enter Credentials", 'error')
            return redirect(url_for('home.login'))
            

#route to logout the user from the session - Adrian 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))
