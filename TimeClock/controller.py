from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, current_app
import threading
# from . import thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

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
                with current_app.app_context():
                    render_template('index.html', read = val)
                GPIO.output(buzzer,GPIO.HIGH)          
                time.sleep(5)
                GPIO.output(buzzer,GPIO.LOW)
    except:
        raise
    finally:
            GPIO.cleanup()

# thread = threading.Thread(target=read)
# thread.start()

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        thread = threading.Thread(target=read)
        thread.start()
        return render_template('index.html', read = False)
    else:
        return render_template('index.html', read = False)

@home.route('/stopReadThread', methods=['POST'])
def stopReadThread():
    # thread.stop()
    return redirect(url_for('home.index'))

@home.route('/userClock/<string:val>', methods=['GET', 'POST'])
def userClock(val):
    print(val)
    return render_template('index.html', read = val )


# @home.route('/read', methods=['GET','POST'])
# def read():
#     print(request.method)
#     print(request.json['text'])
#     if request.json['text'] == '' or request.json == None:
#         print('error')
#         flash("Error En Deteccion", 'error')
#     else:
#         print(request.json['text'])
#         flash(request.json['text'], 'success')

#     print("RENDER?")
#     return redirect(url_for('home.userClock', val = request.json['text']))
#     # render_template('timeUserInput.html', read = request.json['text'])
#     # return "success", 200


