from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
# import threading
from . import thread

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', isActive=True)
    else:
        render_template('index.html')

@home.route('/stopReadThread', methods=['POST'])
def stopReadThread():
    thread.stop()
    return redirect('home.index')
