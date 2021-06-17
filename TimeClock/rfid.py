#!/usr/bin/env python
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from flask import redirect, url_for

reader = SimpleMFRC522()

def write(val):
    try:
        print("Place your tag to write")
        reader.write(val)
        print("Written")
    finally:
        GPIO.cleanup()

def read():
    try:
        while True:
            id, text = reader.read()
            print(id)
            print(text)
            # return redirect(url_for('home.login'))
            time.sleep(5)
    finally:
            GPIO.cleanup()