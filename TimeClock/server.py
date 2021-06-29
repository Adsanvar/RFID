from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify
import threading
# from . import thread
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import webview
import sys
import threading
import json
import os
import requests
from readthread import Reader

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
window = webview.create_window("TimeClock", app, fullscreen=True)
# window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
# base_url = "http://localhost:5000/"

base_url = ""
api_url = "http://192.168.1.65:5005/"

readthread = Reader(window = window, api_url = api_url)

def sendWriteRequest(payload):
    headers= {'content-type': 'application/json'}
    res = requests.get(api_url+"writeFob", data=json.dumps(payload), headers=headers)
    flash(res.text, 'success')

# def start_server():
#     # app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
#     app.run(host='192.168.1.79', port=5000)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'exitWrite' in request.form:
            print("is readthread alive: ", readthread.is_alive())
            # print("from POST, writeropen?: ", writethread.is_alive())
            # startReadThread(False)
            # print("is thread alive: ", thread.is_alive())
            return render_template('index.html')
    else:
        print('Not in exit write')
        return render_template('index.html')

@app.route('/clockin')
@app.route('/clockin/<string:data>')
def clockin(data=None):
    if data != None:
        try:
            headers= {'content-type': 'application/json'}
            res = requests.get(api_url+"clockin", data=data, headers=headers)
            # return jsonify(message='Success')
            return res.text
        except Exception as e:
            print('Exception in /clockin')
            print(e)
            return jsonify(message='Error')
    else:
        return jsonify(message='Error No Data')

@app.route('/getWrite')
@app.route('/getWrite/<string:data>')
def getWrite(data=None):
    if data != None:
        try:
            # headers= {'content-type': 'application/json'}
            # res = requests.get(api_url+"getWrite", data=data, headers=headers)
            # # print(json.dumps(res.text))
            # global read_flag
            # read_flag = False
            # window.load_url(base_url+"writer/"+res.text)

            # global readthread
            loadWriter(data)
            # if readthread.is_alive():
            #     stopReadThread()
            if not readthread.stopped():
                readthread.stop()
            # readthread._stop()
            # print(res.text)
            return "success"
        except Exception as e:
            print('Exception in getWrite')
            print(e)
            raise
            return jsonify(message='Error')
    else:
        return jsonify(message='Error No Data')

def loadWriter(data):
    headers= {'content-type': 'application/json'}
    res = requests.get(api_url+"getWrite", data=data, headers=headers)
    # print(json.dumps(res.text))
    # global read_flag
    # read_flag = False
    window.load_url(base_url+"writer/"+res.text)

@app.route('/writer',methods=['GET', 'POST'])
@app.route('/writer/<string:data>', methods=['GET', 'POST'])
def writer(data=None):
    if request.method == "POST":
        print('inpost')
        data = json.loads(data)
        print(data)
        emp_id = int(request.form.get('id'))
        for emp in data:
            if emp['id'] == emp_id:
                name = emp['firstname'] + ' ' + emp['lastname']
                # data.pop(data.index(emp))
                # startWriteThread(name, emp_id)
                del data[data.index(emp)]
                
        # print("is writeer active: ", writeThread.is_alive())
        if not data:
            return render_template('writer.html')
        else:
            window.load_url(base_url+"writer/"+json.dumps(data))
            return "success"
    else:
        print(data)
        if data != None:
            print("in data not empty")
            try:

                data = json.loads(data)
                print(data)
                for d in data:
                    print(d['firstname'])
                # print("isAlive(): ", readthread.isAlive())
                # print("is_alive(): ", readthread.is_alive())
                # global read_flag
                # read_flag = False
                # print("read_flag = ", read_flag)
                # print("isAlive(): ", readthread.isAlive())
                # print("is_alive(): ", readthread.is_alive())
                # print("_stop.set(): ")
                # readthread._stop()
                # print("isAlive(): ", readthread.isAlive())
                # writethread = threading.Thread(target=write(data))
                # writethread.start()
                # writethread.join()
                # GPIO.cleanup()
                # write(data)
                # read_flag = True
                # global read_flag
                # read_flag = False
                # print("is thread alive?",readthread.is_alive())
                # # stopReadThread()
                # readthread._stop()
                # print("is thread alive?",readthread.is_alive())
                # write(data)
                # read_flag = True
                # startReadThread()
                return render_template('writer.html', data=data)
            except Exception as e:
                print('Exception in GET of /Writer')
                raise
        else:
            print("no data")
            return jsonify(message='Error No Data')


def setBaseUrl():
    global base_url
    base_url = window.get_current_url()
    print("base url: ", base_url)
    readthread.setBaseUrl(base_url)

# def getWriteThread():
#     global writethread
#     return writethread

# def startWriteThread(val, id):
#     global writethread 
#     writethread = threading.Thread(target=write(val, id))
#     print('with global variables startWriteThread(val, id), writethread start')
#     writethread.start()

# def stopWriteThread():
#     global writethread
#     print('with global variables stopWriteThread(), writethread stop')
#     writethread._stop()

# def stopReadThread():
#     global readthread
#     global read_flag

#     read_flag = False
#     print('with global variables stopReadThread(), read_flag== False, readthread stop')
#     readthread._stop()

# def startReadThread(start):
#     # readthread = threading.Thread(target=read)
#     # readthread._stop_event = threading.Event()
#     global readthread
#     global read_flag
#     if start:
#     # readthread.daemon = True
#         print('with global variables from start, readthread start')
#         readthread.start()
#     else:
#         read_flag = True
#         readthread = threading.Thread(target=read)
#         print('with global variables from not start, read_flag== True, readthread start')
#         readthread.start()
        

if __name__ == '__main__':

    # t = threading.Thread(target=start_server)
    # t.daemon = True
    # t.start()
    # startReadThread(True)
    readthread.start()
    # webview.start(setBaseUrl, debug=True)
    webview.start(setBaseUrl)
    sys.exit()