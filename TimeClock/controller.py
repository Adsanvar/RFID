from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, current_app
import threading
# from . import thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import jinja2
import requests, json
import webview

home = Blueprint('home', __name__)

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
            # print(text)
            print(repr(text))
            val = ""
            if text == None or text  == "":
                val = "Error"
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
                # print('\x00' in text)
                if '\x00' in text:
                    val = text.replace('\x00', '')
                else:
                    val = text.rstrip(' ')
                payload = {'id': id, 'text': val}
                print(payload)
                # with current_app.app_context():
                #     render_template('index.html', read = val)
                # template = jinja2.Template('{{ name }} is {{ age }} years old.')
                # rendered = template.render(name='Ginger', age=10)
                sendPost(payload)
                GPIO.output(buzzer,GPIO.HIGH)          
                time.sleep(5)
                GPIO.output(buzzer,GPIO.LOW)
    except:
        raise
    finally:
            GPIO.cleanup()

def sendPost(payload):
    try:
        url = "http://127.0.0.1:5005/read"
        # # url ="http://192.168.1.65:5005/read"
        headers= {'content-type': 'application/json'}
        requests.post(url, data=json.dumps(payload), headers=headers)
        # requests.put(url, data=json.dumps(payload), headers=headers)
        # read(payload)
        # print(payload)
    except Exception as e:
        raise

thread = threading.Thread(target=read)
thread.start()

try:
    webview.create_window("PyWebView & Flask", "https://www.kleene.dev/")
    webview.start()
except Exception as e:
    print(e)
    raise


#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', read = False)
    else:
        return render_template('index.html', read = False)

@home.route('/stopReadThread', methods=['POST'])
def stopReadThread():
    # thread.stop()
    return redirect(url_for('home.index'))

@home.route('/', methods=['GET', 'POST'])
def userClock(val):
    print(val)
    return render_template('index.html', read = val )


@home.route('/read', methods=['GET','POST'])
def read():
    print(request.method)
    print(request.json['text'])
    if request.json['text'] == '' or request.json == None:
        print('error')
        flash("Error En Deteccion", 'error')
    else:
        print(request.json['text'])
        flash(request.json['text'], 'success')

    print("RENDER?")
    return redirect(url_for('home.userClock', read = request.json['text']))
    # render_template('timeUserInput.html', read = request.json['text'])
    return "success"


