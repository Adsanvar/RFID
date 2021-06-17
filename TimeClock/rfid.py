import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import threading
# from flask import redirect, url_for

# reader = SimpleMFRC522()

# def write(val):
#     try:
#         print("Place your tag to write")
#         reader.write(val)
#         print("Written")
#     finally:
#         GPIO.cleanup()

# def read():
#     try:
#         while True:
#             id, text = reader.read()
#             print(id)
#             print(text)
#             # return redirect(url_for('home.login'))
#             time.sleep(5)
#     finally:
#             GPIO.cleanup()

# class RFID(threading.Thread):
# 	def __init__(self):
# 		super().__init__()
#         self.reader = SimpleMFRC522()

# 	# This is whats get called when you do RFID().start()
# 	def run(self):
#         try:
#             while True:
#                 id, text = self.reader.read()
#                 print(id)
#                 print(text)
#                 # return redirect(url_for('home.login'))
#                 time.sleep(5)
#         finally:
#                 GPIO.cleanup()
    
#     def write(val):
#         try:
#             print("Place your tag to write")
#             self.reader.write(val)
#             print("Written")
#         finally:
#             GPIO.cleanup()

# RFID().start()

class RFID(threading.Thread):
    def __init__(self):
        super().__init__()
        self.reader = SimpleMFRC522()
        self._stop_event = threading.Event()
        print("New Class created")
    
    def run(self):
        try:
            print("in run.")
            print("stopped? {}".format(self.stopped))
            while not self.stopped:
                print("Ready For Next")
                id, text = self.reader.read()
                print(id)
                print(text)
                # return redirect(url_for('home.login'))
                time.sleep(5)
        except:
            raise
        finally:
                GPIO.cleanup()

    def stop(self):
        print('thread stropped')
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def write(self, val):
        try:
            print("Place your tag to write")
            self.reader.write(val)
            print("Written")
        except:
            raise
        finally:
            GPIO.cleanup()
    

