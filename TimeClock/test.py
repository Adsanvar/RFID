from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, current_app
import threading
# from . import thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import webview
import sys
import threading
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_secret_key'

window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
base_url = "http://localhost:5000/"
def read():
    try:
        reader = SimpleMFRC522()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        buzzer = 11
        GPIO.setup(buzzer, GPIO.OUT)
        print("in run.")
        while True:
            print("Ready For Next")
            id, text = reader.read()
            print(id)
            print(text)
            # print(repr(text))
            val = ""
            if text == None or text  == '':
                val = "Error"
            else:
                # print('\x00' in text)
                if '\x00' in text:
                    val = text.replace('\x00', '')
                else:
                    val = text.rstrip(' ')

            if val == '':
                val = "Error"
                payload = {'id': id, 'text': val}
                loadOptions(window, payload)
                GPIO.output(buzzer,GPIO.HIGH)              
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.LOW)            
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.HIGH)
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.LOW)
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.HIGH)
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.LOW)
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.HIGH)
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.LOW)
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.HIGH)
                time.sleep(.5)
                GPIO.output(buzzer,GPIO.LOW)
            else:
                payload = {'id': id, 'text': val}
                loadOptions(window, payload)
                GPIO.output(buzzer,GPIO.HIGH)          
                time.sleep(5)
                GPIO.output(buzzer,GPIO.LOW)
    except:
        raise
    finally:
            GPIO.cleanup()

def loadOptions(window, payload):
    url = base_url + json.dumps(payload)
    print(url)
    window.load_url(url)

def start_server():
    # app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
    app.run(host='0.0.0.0', port=5000)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:data>', methods=['GET', 'POST'])
def index(data=None):
    if data != None:
        data = json.loads(data)
        print(data)
        if data['text'] == 'Error':
            flash("Error Leyendo Etiqueta", 'error')
            return render_template('index.html', read = False)
        else:
            return render_template('index.html', read = data['text'])
    else:
        return render_template('index.html', read = False)


if __name__ == '__main__':

    print(os.getcwd())

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    r = threading.Thread(target=read)
    r.daemon = True
    r.start()

    webview.start()
    # webview.load_css()
    sys.exit()