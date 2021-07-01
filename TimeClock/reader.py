import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import threading
import requests
import json
import pyautogui
from gui import loadOptions
from utilities import getserial

class Reader(threading.Thread):
    def __init__(self, window, api_url):
        super().__init__()
        # self.reader = SimpleMFRC522()
        self._stop_event = threading.Event()
        self.window = window
        self.api_url = api_url
        # self.read_flag = True
        print("New Class created")    

    def stop(self):
        print('Read thread stropped')
        # GPIO.cleanup()
        self._stop_event.set()

    def resume(self):
        print("Resume")
        self._stop_event.clear()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        try:
            # GPIO.cleanup()
            reader = SimpleMFRC522()
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            buzzer = 11
            GPIO.setup(buzzer, GPIO.OUT)
            print("in run.")
            while not self._stop_event.isSet():
            # while self.read_flag:
                # print(self.read_flag)
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
                    loadOptions(self.window, payload, self.base_url, self.api_url)
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
                    loadOptions(self.window, payload, self.base_url, self.api_url)
                    # print(window.get_current_url())
                    GPIO.output(buzzer,GPIO.HIGH)          
                    time.sleep(3)
                    GPIO.output(buzzer,GPIO.LOW)
                    if val == "Admin":
                        print("Reader Read Admin, stopping read thread")
                        # self.read_flag = False
                        self._stop_event.set()
        except:
            print('read exception')
            raise
        finally:
            GPIO.cleanup()
    
    def setBaseUrl(self, base_url):
        self.base_url = base_url
        print("base url set: ", self.base_url)