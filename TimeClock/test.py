from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, current_app
import threading
# from . import thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import webview
import sys
import threading

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', read = False)
    else:
        return render_template('index.html', read = False)

def start_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("PyWebView & Flask", "http://localhost:5000/")
    webview.start()
    sys.exit()