import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import threading
import requests
import json
import pyautogui
from .utilities import getserial
from .server import loadOptions
# rf = Blueprint('rfid', __name__)

class Reader(threading.Thread):
    def __init__(self, window):
        super().__init__()
        self.reader = SimpleMFRC522()
        self._stop_event = threading.Event()
        self.window = window
        print("New Class created")
    

    def stop(self):
        print('thread stropped')
        GPIO.cleanup()
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        try:
            reader = SimpleMFRC522()
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            buzzer = 11
            GPIO.setup(buzzer, GPIO.OUT)
            print("in run.")
            while not self._stop_event.isSet():
                print("Ready For Next")
                id, text = reader.read()
                print(id)
                print(text)
                print(repr(text))
                pyautogui.moveTo(512, 300) #moves mouse to center to invoke a wake up rpi if it is sleeping
                val = ""
                if text == None or text  == '':
                    val = "Error"
                else:
                    # print('\x00' in text)
                    if '\x00' in text:
                        val = text.replace('\x00', '')
                    else:
                        val = text.rstrip(' ')

                if val == '' or val == None:
                    val = "Error"
                    payload = {'id': id, 'text': val}
                    loadOptions(self.window, payload)
                    # print(window.get_current_url())
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
                    payload = {'id': id, 'text': val, 'device': getserial()}
                    loadOptions(self.window, payload)
                    # print(window.get_current_url())
                    GPIO.output(buzzer,GPIO.HIGH)          
                    time.sleep(3)
                    GPIO.output(buzzer,GPIO.LOW)
        except:
            print('read exception')
            raise
        finally:
                GPIO.cleanup()

        # try:
        #     GPIO.setwarnings(False)
        #     GPIO.setmode(GPIO.BOARD)
        #     buzzer = 11
        #     GPIO.setup(buzzer, GPIO.OUT)
        #     print("in run.")
        #     while not self._stop_event.isSet():
        #         print("Ready For Next")
        #         id, text = self.reader.read()
        #         print(id)
        #         # print(text)
        #         print(repr(text))
        #         val = ""
        #         if text == None or text  == "":
        #             val = "Error"
        #             GPIO.output(buzzer,GPIO.HIGH)              
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.LOW)            
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.HIGH)
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.LOW)
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.HIGH)
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.LOW)
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.HIGH)
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.LOW)
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.HIGH)
        #             time.sleep(.5)
        #             GPIO.output(buzzer,GPIO.LOW)
        #         else:
        #             print('\x00' in text)
        #             if '\x00' in text:
        #                 val = text.replace('\x00', '')
        #             else:
        #                 val = text.rstrip(' ')
        #             payload = {'id': id, 'text': val}
        #             self.sendPost(payload)
        #             GPIO.output(buzzer,GPIO.HIGH)              
        #             time.sleep(5)
        #             GPIO.output(buzzer,GPIO.LOW)
        # except:
        #     raise
        # finally:
        #         GPIO.cleanup()

    # def write(self, val):
    #     try:
    #         print("Place your tag to write")
    #         self.reader.write(val)
    #         print("Written")
    #     except:
    #         raise
    #     finally:
    #         GPIO.cleanup()

    # def sendPost(self, payload):
    #     try:
    #         # url = "http://127.0.0.1:5005/read"
    #         # # url ="http://192.168.1.65:5005/read"
    #         # headers= {'content-type': 'application/json'}
    #         # requests.post(url, data=json.dumps(payload), headers=headers)
    #         # requests.put(url, data=json.dumps(payload), headers=headers)
    #         # read(payload)
    #         print(payload)
    #     except Exception as e:
    #         raise
    
# @rf.route('/read<string:payload>')
# def read(payload):
#     # print(request.method)
#     # print(request.json['text'])
#     # if request.json['text'] == '' or request.json == None:
#     #     print('error')
#     #     flash("Error En Deteccion", 'error')
#     # else:
#     #     print(request.json['text'])
#     #     flash(request.json['text'], 'success')

#     # print("RENDER?")
#     # return redirect(url_for('home.userClock', val = request.json['text']))
#     print(payload)
#     return render_template('index.html', read = "HELLO")
