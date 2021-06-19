from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
# import threading
from . import thread

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', read = False)
    else:
        return render_template('index.html', read = False)

@home.route('/stopReadThread', methods=['POST'])
def stopReadThread():
    thread.stop()
    return redirect(url_for('home.index'))
@home.route('/<string:val>', methods=['GET', 'POST'])
def userClock(val):
    return render_template('index.html', read = val )

@home.route('/read', methods=['POST'])
def read():
    print(request.method)
    if request.json['text'] == '' or request.json == None:
        print('error')
        flash("Error En Deteccion", 'error')
    else:
        print(request.json['text'])
        flash(request.json['text'], 'success')

    print("RENDER?")
    return redirect(url_for('home.userClock', val = request.json['text']))
    # return render_template('index.html', read = request.json['text'] )
