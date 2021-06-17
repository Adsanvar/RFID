#!/usr/bin/env python
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# def write(val):
#     try:
#         print("Place your tag to write")
#         reader.write(val)
#         print("Written")
#     finally:
#         GPIO.cleanup()

try:
    val = "ADRIAN SANDOVAL-VARGAS"
    print("Place your tag to write")
    reader.write(val)
    print("Written")
finally:
    GPIO.cleanup()

# def read():
#     try:
#         id, text = reader.read()
#         print(id)
#         print(text)
#     finally:
#             GPIO.cleanup()

try:
    id, text = reader.read()
    print(id)
    print(text)
finally:
        GPIO.cleanup()