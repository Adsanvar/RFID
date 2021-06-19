import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import threading
import requests
import json
from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for

rfid = Blueprint('rfid', __name__)

class RFID(threading.Thread):
    def __init__(self):
        super().__init__()
        self.reader = SimpleMFRC522()
        self._stop_event = threading.Event()
        print("New Class created")
    

    def stop(self):
        print('thread stropped')
        GPIO.cleanup()
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            buzzer = 11
            GPIO.setup(buzzer, GPIO.OUT)
            print("in run.")
            while not self._stop_event.isSet():
                print("Ready For Next")
                id, text = self.reader.read()
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
                    print('\x00' in text)
                    if '\x00' in text:
                        val = text.replace('\x00', '')
                    else:
                        val = text.rstrip(' ')
                    payload = {'id': id, 'text': val}
                    self.sendPost(payload)
                    GPIO.output(buzzer,GPIO.HIGH)              
                    time.sleep(5)
                    GPIO.output(buzzer,GPIO.LOW)
        except:
            raise
        finally:
                GPIO.cleanup()

    def write(self, val):
        try:
            print("Place your tag to write")
            self.reader.write(val)
            print("Written")
        except:
            raise
        finally:
            GPIO.cleanup()

    def sendPost(self, payload):
        try:
            url = "http://127.0.0.1:5005/read"
            # url ="http://192.168.1.65:5005/read"
            headers= {'content-type': 'application/json'}
            # requests.post(url, data=json.dumps(payload), headers=headers)
            requests.put(url, data=json.dumps(payload), headers=headers)
        except Exception as e:
            raise
    
@home.route('/read', methods=['PUT'])
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
    return redirect(url_for('home.userClock', val = request.json['text']))
