import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import threading
import requests
import json

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
            print("in run.")
            while not self._stop_event.isSet():
                print("Ready For Next")
                id, text = self.reader.read()
                print(id)
                print(text)
                self.id = id
                self.text = text
                # return redirect(url_for('home.login'))
                time.sleep(5)
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

    def sendPost(self, info):
        url = "http://localhost:5005/read"
        requests.post(url, data=json.dumps(info))
    

