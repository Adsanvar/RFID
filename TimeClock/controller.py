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
    return redirect(url_for('home.index'))

@home.route('/read', methods=['POST'])
def read():
    # info = request.args.get("data")
    if request.json.text == '' or request.json == None:
        flash("Error En Deteccion", 'error')
    else:
        flash(request.json.text, 'success')

    return redirect(url_for('home.index'))
