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
        super.__init__()
        self.reader = SimpleMFRC522()
    
    def run(self):
        try:
            while True:
                id, text = self.reader.read()
                print(id)
                print(text)
                # return redirect(url_for('home.login'))
                time.sleep(5)
        finally:
                GPIO.cleanup()

    def write(self, val):
        try:
            print("Place your tag to write")
            self.reader.write(val)
            print("Written")
        finally:
            GPIO.cleanup()
