from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, current_app
import threading
# from . import thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import webview
import sys
import threading

app = Flask(__name__)
window = webview.create_window("PyWebView & Flask", "http://localhost:5000/", fullscreen=True)

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
                # with current_app.app_context():
                #     render_template('index.html', read = val)
                # template = jinja2.Template('{{ name }} is {{ age }} years old.')
                # rendered = template.render(name='Ginger', age=10)
                # sendPost(payload)
                GPIO.output(buzzer,GPIO.HIGH)          
                time.sleep(5)
                GPIO.output(buzzer,GPIO.LOW)
    except:
        raise
    finally:
            GPIO.cleanup()

def start_server():
    app.run(host='0.0.0.0', port=5000)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', read = False)
    else:
        return render_template('index.html', read = False)


if __name__ == '__main__':

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    r = threading.Thread(target=read)
    r.daemon = True
    r.start()

    webview.start()
    sys.exit()