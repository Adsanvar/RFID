from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
import TimeClock.rfid as RFID
# import threading


home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', isActive=True)
    else:
        render_template('index.html')
