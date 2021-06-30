import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


try:
    writerx = SimpleMFRC522()
    print("Now place your tag to write")
    writerx.write("Admin")
    print('written')
except:
    print('write exception')
    raise
finally:
    GPIO.cleanup()