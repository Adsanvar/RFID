from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, jsonify
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import webview
import sys
import threading
import json
import os
import requests
from reader import Reader
from writer import Writer
from utilities import getserial
import gui 
import datetime
from pathlib import Path
import logging
import csv
from flask_apscheduler import APScheduler


now = datetime.datetime.now()
Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename = '{}/{}.log'.format('logs', now), level=logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
scheduler = APScheduler()
scheduler.start()

config = None
fobs = None

try:
    # f = open('/home/pi/Documents/rfid/timeClockConfig.json', 'r')
    f = open('/home/pi/Documents/rfid/devTimeClockConfig.json', 'r')
    config = json.load(f)
    app.logger.info('Config File Loaded')
    f.close()
except Exception as e:
    print('error occurred reading file')
    app.logger.error('Config File Error')
    app.logger.error(e)
    raise
    

app.config['SECRET_KEY'] = config['secret_key']
window = webview.create_window("TimeClock", app, fullscreen=True)
# window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
# base_url = "http://localhost:5000/"

base_url = ""
# api_url = "http://192.168.1.65:5005/"
api_url = config['api_url']


def getFobs(api_url):
    try:
        payload = {"device": getserial()}
        headers= {'content-type': 'application/json'}
        data = json.dumps(payload)
        res = requests.get(api_url+"getFobs", data=data, headers=headers)
        res = json.loads(res.text)
        return res

    except Exception as e:
        print('Exception in getFobs')
        print(e)
        app.logger.error("Exception Trying to Get fobs")
        return False

def loadFobs():
    try:
        objs = getFobs(api_url)
        if objs != False:
            with open('/home/pi/Documents/rfid/fobs.json', 'w+', encoding='utf-8') as f:
                json.dump(objs, f, ensure_ascii=False, indent=4)

    except Exception as e:
        app.logger.error("Exception Trying to load fobs")
        print(e)

loadFobs()

readthread = Reader(window = window, api_url = api_url)
readthread.daemon = True
# writethread = Writer(api_url=api_url)
# writethread.daemon = True

# success_flag = False

# def start_server():
#     # app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
#     app.run(host='192.168.1.79', port=5000)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.args.get('data')
    if data != None:
        if data == 'fromStopWrite':
            app.logger.info('Stopping From a Write Operation')
            window.load_url(base_url)
            readthread.resume()
            app.logger.info('Resuming ReadThread and Running it again')
            readthread.run()
        elif data == 'closeHours':
            app.logger.info('Loading base url from close hours')
            window.load_url(base_url)
        return 'success'
    else:
        return render_template('index.html')

@app.route('/clockin')
@app.route('/clockin/<string:data>')
def clockin(data=None):
    if data != None:
        try:
            # Code to send to server
            # headers= {'content-type': 'application/json'}
            # res = requests.get(api_url+"clockin", data=data, headers=headers)
            # # return jsonify(message='Success')
            # return res.text

            data = json.loads(data)
            dt = datetime.datetime.now()
            with open(f'/home/pi/Documents/rfid/{dt.year}_TimeClock.csv', 'a+') as f:
                clkin = csv.writer(f, delimiter=',')
                # header = ['date', 'name','fobid', 'in/out','time', 'lunch']
                # clkin.writerow(header)
                row = [dt.date(), data['text'], data['id'], 'in', dt, False]
                clkin.writerow(row)
                f.close()
            
            return jsonify(message='Success')

        except Exception as e:
            print('Exception in /clockin')
            print(e)
            app.logger.error('Exception in /clockin, {}'.format(e))
            return jsonify(message='Error')
    else:
        app.logger.warning('No Data in clockin')
        return jsonify(message='Error No Data')

@app.route('/clockout')
@app.route('/clockout/<string:data>')
def clockout(data=None):
    if data != None:
        try:
            # headers= {'content-type': 'application/json'}
            # res = requests.get(api_url+"clockout", data=data, headers=headers)
            # # return jsonify(message='Success')
            # return res.text

            data = json.loads(data)
            dt = datetime.datetime.now()
            with open(f'/home/pi/Documents/rfid/{dt.year}_TimeClock.csv', 'a+') as f:
                clkin = csv.writer(f, delimiter=',')
                row = [dt.date(), data['text'], data['id'],'out', dt, data['lunch']]
                clkin.writerow(row)
                f.close()

            return jsonify(message="Success")

        except Exception as e:
            print('Exception in /clockout')
            print(e)
            app.logger.error('Exception in /clockout, {}'.format(e))
            return jsonify(message='Error')
    else:
        app.logger.warning('No Data in clockout')
        return jsonify(message='Error No Data')    

@app.route('/resumeRead', methods=['GET'])
def resumeRead():
    readthread.resume()
    readthread.run()
    return jsonify(message='success')

@app.route('/getHours')
@app.route('/getHours/<string:data>')
def getHours(data=None):
    try:
        app.logger.info('Loading Hours')
        loadHours(data)
        return jsonify(message='success')
    except Exception as e:
        print('Exception in getHours')
        print(e)
        app.logger.warning("Exception in getHours")
        return jsonify(message='Error')

@app.route('/hours')
@app.route('/hours/<string:data>')
def hours(data=None):
    if data != None:
        try:
            res = json.loads(data)
            data_table = {}
            for i in res:
                if res[i]['clock_in'] is not None or res[i]['clock_in'] != '':
                    clk_in = datetime.datetime.strptime(res[i]['clock_in'], '%a, %d %b %Y %H:%M:%S GMT').strftime("%I:%M:%S %p")
                    clk_out = datetime.datetime.strptime(res[i]['clock_out'], '%a, %d %b %Y %H:%M:%S GMT').strftime("%I:%M:%S %p")
                else:
                    clk_in = res[i]['clock_in']
                    clk_out = res[i]['clock_out']
                    
                date = res[i]['date']
                hours = res[i]['hours']
                if res[i]['no_lunch']:
                    lunch = "NO"
                else:
                    lunch = "SI"
                data_table[i] = {}
                data_table[i]['date'] = date
                data_table[i]['clk_in'] = clk_in
                data_table[i]['clk_out'] = clk_out
                data_table[i]['hours'] = hours
                data_table[i]['no_lunch'] = lunch
            
            return render_template("hours.html", data=data)
        except Exception as e:
            print('Exception in load hours')
            print(e)
            app.logger.warning("Exception in loadhours")
            return jsonify(message='Error')
    else:
        app.logger.info("No Data coming into loadhours")
        return jsonify(message='Error No Data') 

def loadHours(data):
    data = json.loads(data)
    print("in loadHours: ", data)
    payload = {"device": getserial() "id": data}
    headers= {'content-type': 'application/json'}
    data = json.dumps(payload)
    res = requests.get(api_url+"getHours", data=data, headers=headers)
    window.load_url(base_url+"hours/"+res) 

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
            # readthread.stop() # prevents erroneous stoppage of readthread from http request to validate fob

            loadWriter(data)
            # if readthread.is_alive():
            #     stopReadThread()
            # print("Get Write: is readthread alive? ", readthread.is_alive())
            # print("Get Write: is readthread stopped? ", readthread.stopped())
            app.logger.info('Get Write: is readthread alive? {}'.format(readthread.is_alive()))
            app.logger.info('Get Write: is readthread alive? {}'.format(readthread.stopped()))
            # if not readthread.stopped():
            #     readthread.stop()
            # print("is readthread alive? ", readthread.is_alive())
            # print("is readthread stopped? ", readthread.stopped())
            # readthread._stop()
            # print(res.text)
            return jsonify(message='success')
        except Exception as e:
            print('Exception in getWrite')
            print(e)
            app.logger.warning("Exception in getWrite")
            return jsonify(message='Error')
    else:
        app.logger.info("No Data coming into getWrite")
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
                print('found')
                name = emp['firstname'] + ' ' + emp['lastname']
                # data.pop(data.index(emp))
                # startWriteThread(name, emp_id)
                # wr = threading.Thread(target = write(name, emp['id']))
                # wr.start()
                # print("is write thread alive? ", wr.is_alive())
                # wr.join()
                #print(threading.current_thread().name)

                # if writethread.is_alive():
                #     print('writer: in run')
                #     writethread.run()
                # else:
                #     print('writer: in start')
                #     writethread.start()
                # print("writer: alive? ", writethread.is_alive())
                # writethread.setWriter(name, emp_id)
                # writethread.setWriteFlag(True)
                # writethread.write()
                # print("After write thread")
                # print('writer: running')
                # writethread.run()
                # print('Proceeding after run')
                val = write(name, emp_id)

                if not val:
                    break
                
                del data[data.index(emp)]
              
        # print("is writeer active: ", writeThread.is_alive())
        if val:
            if not data:
                flash('There are no more employees to write', 'warning')
                return render_template('writer.html')
            else:
                window.load_url(base_url+"writer/"+json.dumps(data))
                return "success"
        else:
            flash('error writing key', 'error')
            return render_template('writer.html')
    else:
        if data != None:
            print("in data not empty")
            try:
                print("Writer: is readthread alive: ", readthread.is_alive())
                print("Writer: is readthread stopped? ", readthread.stopped())
                data = json.loads(data)
                print(data)
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
                app.logger.error("Exception in GET Writer")
                app.logger.error(e)
        else:
            print("no data")
            app.logger.warning("No Data Comming into Writer")
            return jsonify(message='Error No Data')

def write(val, empId):
    try:
        # print(threading.current_thread().name)
        GPIO.cleanup()
        print('place to read')
        readerx = SimpleMFRC522()
        id, text = readerx.read()

        if "Admin" in text:
            payload = {"id":id, "text": "Admin", "device": getserial()}
            res = gui.validateFob(payload, api_url)
            if res:
                return False
        

        GPIO.cleanup()        
        writerx = SimpleMFRC522()
        print("Now place your tag to write")
        writerx.write(val)
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BOARD)
        # buzzer = 11
        # GPIO.setup(buzzer, GPIO.OUT)
        # GPIO.output(buzzer,GPIO.HIGH)
        # time.sleep(2)
        # GPIO.output(buzzer,GPIO.LOW)
        print("Base level Written")
        payload = {'id': id, 'text': val, 'device': getserial(), 'employeeId': empId}
        gui.sendWriteRequest(payload, api_url)
        return True
    except Exception as e:     
        print('write exception')
        print(e)
        app.logger.error("Write Function from RFID")
        app.logger.error(e)
    finally:
        GPIO.cleanup()


@app.route('/stopWrite', methods=["POST"])
def stopWrite():
    # writethread.stop()
    print("at stopWrite")

    print("Cancel: is readthread alive: ", readthread.is_alive())
    print("Cancel: is readthread stopped? ", readthread.stopped())
    # print("Cancel: is writethread alive: ", writethread.is_alive())
    # print("Cancel: is writethread stopped? ", writethread.stopped())
    loadFobs()
    return redirect(url_for('index', data="fromStopWrite"))


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
        

# @app.route('/csvProcessor', methods=['POST'])
@scheduler.task('cron', id='csvProcessor', hour="23", minute='00')
def csvProcessor():
    now = datetime.datetime.now()
    # delta = now + datetime.timedelta(minutes = 1)
    # sleep(15)
    app.logger.info("Processing CSV FILE - START: {} ".format(now))
    dt = datetime.datetime.now()
    data = {}
    try:
        with open(f'/home/pi/Documents/rfid/{dt.year}_TimeClock.csv', 'r') as f: 
            csv_reader = csv.DictReader(f)
            line_count = 0
            for row in csv_reader:
                # print(row)
                # print(dt.date())
                # print(row['date'])
                if row['date'] == f'{dt.date()}':
                    data[line_count] = row['date'], row['name'], row['fobid'], row['in/out'], row['time'], row['nolunch']
                    # print(f"\t{row['date']}, {row['name']}, {row['fobid']}, {row['in/out']}, {row['time']}, {row['lunch']}")
                    # line_count += 1
                    line_count += 1
            print(line_count)
            f.close()
        data['device'] = getserial()
        data = json.dumps(data)
        # print(data)
        headers= {'content-type': 'application/json'}
        res = requests.get(api_url+"processCsv", data=data, headers=headers)
        res = json.loads(res.text)
        # print(res['message'])
            
        app.logger.info("Processing CSV FILE - ENDED: {}".format(now))
        return render_template('index.html')
    except:
        raise

if __name__ == '__main__':
    try:
        # t = threading.Thread(target=start_server)
        # t.daemon = True
        # t.start()
        # startReadThread(True)
        readthread.start()
        # writethread.setWriteFlag(False)
        # writethread.start()
        app.logger.info("Read Thread Started")
        # webview.start(setBaseUrl, debug=True)
        app.logger.info("starting the webview window with a base url")
        webview.start(setBaseUrl)
        sys.exit()
    except Exception as e:
        app.logger.error("Error Running the __main__ thread")
        app.logger.error(e)
        raise
        