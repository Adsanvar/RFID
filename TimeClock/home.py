from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify, send_file, Response
import webview
from TimeClock.reader import Reader
from TimeClock.writer import Writer
from TimeClock.utilities import getserial
import TimeClock.gui
import datetime

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')

def create():
    window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
    readthread = Reader(window = window, api_url = api_url)
    readthread.daemon = True