from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
import TimeClock.rfid as RFID
import threading
from multiprocessing import Process

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # read()
        # p = Process(target=RFID.read())
        # p.daemon = True
        # p.start() 
        # target=RFID.read()
        read()
        return render_template('index.html', isActive=True)
    else:
        render_template('index.html')

def read():
    x = threading.Thread(target=RFID.read())
    x.start()