#!/usr/bin/python3
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
from read_v2 import Reader as readx
from utilities import getserial
import gui 
import datetime
from pathlib import Path
import logging
import csv
from flask_apscheduler import APScheduler
from time import sleep
#import pandas as pd

now = datetime.datetime.now()
Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename = '{}/{}.log'.format('logs', now), level=logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
scheduler = APScheduler()
scheduler.start()

config = None
fobs = None

# prod
try:
    f = open('/home/pi/Documents/RFID/TimeClock/config.json', 'r')
    # f = open('/home/pi/Documents/rfid/devTimeClockConfig.json', 'r')
    config = json.load(f)
    app.logger.info('Config File Loaded')
    f.close()
except Exception as e:
    print('error occurred reading file')
    app.logger.error('Config File Error')
    app.logger.error(e)
    raise
    
# prod
app.config['SECRET_KEY'] = config['secret_key']
# devel
# app.config['SECRET_KEY'] = "TESTSECRETKEY"

# prod
window = webview.create_window("TimeClock", app, fullscreen=True)

# devel
# window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
# base_url = "http://localhost:5000/"

# prod
base_url = ""
api_url = config['api_url']

# devel
# api_url = "http://localhost:5000/"

def getFobs(api_url=None):
    try:
        payload = {"device": getserial()}
        sleep(5)
        headers= {'content-type': 'application/json'}
        data = json.dumps(payload)
        res = requests.get(api_url+"getFobs", data=data, headers=headers)
        res = json.loads(res.text)
        app.logger.info('getFobs REPONSE:')
        app.logger.info(res)
        return res

    except Exception as e:
        print('Exception in getFobs')
        print(e)
        app.logger.exception("Exception Trying to Get fobs")
        return False

def loadFobs():
    try:
        app.logger.info("GETTING FOBS")
        objs = getFobs(api_url)
        # print("Response: ", objs, "TYPE: ", type(objs), type(objs['message']))
        # print("Response: ", objs, "TYPE: ", type(objs))
        if type(objs) != dict:
            # print("Response: ", objs)
            with open('/home/pi/Documents/RFID/fobs.json', 'w+', encoding='utf-8') as f:
                json.dump(objs, f, ensure_ascii=False, indent=4)
            app.logger.info("LOADED FOBS")
        else:
            for i in range(10):
                objs = getFobs(api_url)
                # print("Retry Response: ", objs)
                if len(objs) != 1 and len(objs[0]) != 1:
                    with open('/home/pi/Documents/RFID/fobs.json', 'w+', encoding='utf-8') as f:
                        json.dump(objs, f, ensure_ascii=False, indent=4)
                    break
                else:
                    sleep(10)
                    continue
    except Exception as e:
        app.logger.exception("Exception Trying to load fobs")
        print(e)



# MAIN

# readthread = Reader(window = window, api_url = api_url)
# readthread.daemon = True

# END MAIN

readthread = readx(window = window, api_url = api_url)

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
            # readthread.resume()
            app.logger.info('Resuming ReadThread and Running it again')
            readthread.run()
        elif data == 'closeHours':
            app.logger.info('Loading base url from close hours')
            window.load_url(base_url)
            app.logger.info('Setting not_in_hours flag for reading')
            # readthread.not_in_hours()
        return 'success'
    else:
        # print(loadFobs())
        # tc = dbc.Timeclock(fobid=123, date=datetime.datetime.now(), clockin=datetime.datetime.now(), nolunch=False)
        # dbc.createTimeclock(tc)
        # print(dbc.getTimeclockRowById(123))
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
            dt = datetime.datetime.now().replace(microsecond=0)
            with open(f'/home/pi/Documents/RFID/TimeClock/{dt.year}_TimeClock.csv', 'a+') as f:
                clkin = csv.writer(f, delimiter=',')
                f.seek(0)
                r = f.read(2)
                print(r)
                print(len(r))
                if len(r) == 0:
                    header = ['date', 'name','fobid', 'in/out','time', 'nolunch']
                    clkin.writerow(header)
                row = [dt.date(), data['text'], data['id'], 'in', dt, False]
                clkin.writerow(row)
                f.close()
            
            return jsonify(message='Success')

        except Exception as e:
            print('Exception in /clockin')
            print(e)
            app.logger.error('Exception in /clockin, {}'.format(e))
            app.logger.exception("Exception in /clocking")
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
            dt = datetime.datetime.now().replace(microsecond=0)
            with open(f'/home/pi/Documents/RFID/TimeClock/{dt.year}_TimeClock.csv', 'a+') as f:
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
    # readthread.resume()
    # readthread.run()
    return jsonify(message='success')

# hours feature has be disabled
# @app.route('/getHours')
# @app.route('/getHours/<string:data>')
# def getHours(data=None):
#     try:
#         app.logger.info('Loading Hours')
#         print("loading hours")
#         loadHours(data)
#         return jsonify(message='success')
#     except Exception as e:
#         print('Exception in getHours')
#         print(e)
#         app.logger.warning("Exception in getHours")
#         window.load_url(base_url) 
#         return jsonify(message='getHour Error')

@app.route('/hours')
@app.route('/hours/<string:data>')
def hours(data=None):
    if data != None:
        try:
            res = json.loads(data)
            print('in hours')
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
            
            # print(data_table)
            # app.logger.info('Stopping ReadThread')
            # readthread.in_hours()
            return render_template("hours.html", data=data_table)
        except Exception as e:
            print('Exception in load hours')
            print(e)
            app.logger.warning("Exception in loadhours: {}".format(e))
            window.load_url(base_url) 
            return jsonify(message='Error')
    else:
        app.logger.info("No Data coming into loadhours")
        window.load_url(base_url) 
        return jsonify(message='Error No Data') 

# TODO: LOAD hours from csv file.
def loadHours(data):
    # try:
    #     dt = datetime.datetime.now()
    #     before = dt - datetime.timedelta(weeks=3)
    #     df = pd.read_csv(f'/home/pi/Documents/rfid/{dt.year}_TimeClock.csv',header=0)
    #     df[(df['date']> str(before.date())) & (df['date']< str(dt.date())) & (df['fobid'] == data)]
    #     df = df.drop(['fobid'], axis=1)
    #     df['in/out'] = df['in/out'].map({'in':'Entrada' ,'out':'Salida'})
    #     df['lunch'] = df['lunch'].map({False:'Si' ,True:'No'})
    #     df.columns = ['Fecha', 'Nombre', 'Entrada/Salida', 'Tiempo', "Almuerzo"]
    #     dct = df.to_dict()
    #     data = json.dumps(dct)
    #     window.load_url(base_url+"hours/"+data)
    # except Exception as e:
    #     print(e)
    #     window.load_url(base_url)
    try:
        data = json.loads(data)
        payload = {"device": getserial(), "fobid": data}
        headers= {'content-type': 'application/json'}
        data = json.dumps(payload)
        res = requests.get(api_url+"getHours", data=data, headers=headers)
        val = json.loads(res.text)
        
        if 'message' not in val:
            window.load_url(base_url+"hours/"+res.text) 
        else:
            window.load_url(base_url)
    except Exception as e:
        print(f'Exception in loadHours {e}')
        window.load_url(base_url) 

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


            # ------------- main
            # app.logger.info('Get Write: is readthread alive? {}'.format(readthread.is_alive()))
            # app.logger.info('Get Write: is readthread alive? {}'.format(readthread.stopped()))
            # ------------- end main


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
        return jsonify(message='Error No Data'), 400

def loadWriter(data):
    headers= {'content-type': 'application/json'}
    res = requests.get(api_url+"getWrite", data=data, headers=headers)
    app.logger.warning("loadWriter Info", res)
    # print(json.dumps(res.text))
    # global read_flag
    # read_flag = False
    window.load_url(base_url+"writer/"+res.text)

@app.route('/writer',methods=['GET', 'POST'])
@app.route('/writer/<string:data>', methods=['GET', 'POST'])
def writer(data=None):
    # POST = write request to api
    if request.method == "POST":
        app.logger.info('/writer POST')
        data = json.loads(data)
        app.logger.info(data)
        emp_id = int(request.form.get('id'))
        for emp in data:
            if emp['id'] == emp_id:
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
        # To display fobs to write
        if data != None:
            try:
                # ---------- MAIN
                # app.logger.info("Writer: is readthread alive: ", readthread.is_alive())
                # app.logger.info("Writer: is readthread stopped? ", readthread.stopped())
                # ---------- END MAIN

                data = json.loads(data)
                app.logger.info(data)
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
                app.logger.exception("Exception in GET Writer")
                app.logger.error(e)
        else:
            app.logger.warning("No Data Comming into Writer")
            return jsonify(message='Error No Data')

def write(val, empId):
    try:
        # print(threading.current_thread().name)
        GPIO.cleanup()
        readerx = SimpleMFRC522()
        id, text = readerx.read()

        if "Admin" in text:
            payload = {"id":id, "text": "Admin", "device": getserial()}
            res = gui.validateFob(payload, api_url)
            if res:
                return False

        GPIO.cleanup()        
        writerx = SimpleMFRC522()
        writerx.write(val)
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BOARD)
        # buzzer = 11
        # GPIO.setup(buzzer, GPIO.OUT)
        # GPIO.output(buzzer,GPIO.HIGH)
        # time.sleep(2)
        # GPIO.output(buzzer,GPIO.LOW)
        payload = {'id': id, 'text': val, 'device': getserial(), 'employeeId': empId}
        gui.sendWriteRequest(payload, api_url)
        return True
    except Exception as e:     
        app.logger.exception("Write Function from RFID")
        app.logger.error(e)
    finally:
        GPIO.cleanup()


@app.route('/stopWrite', methods=["POST"])
def stopWrite():
    # writethread.stop()

    app.logger.info("Cancel: is readthread alive: ", readthread.is_alive())
    app.logger.info("Cancel: is readthread stopped? ", readthread.stopped())
    # print("Cancel: is writethread alive: ", writethread.is_alive())
    # print("Cancel: is writethread stopped? ", writethread.stopped())
    loadFobs()
    return redirect(url_for('index', data="fromStopWrite"))


def setBaseUrl():
    global base_url
    base_url = window.get_current_url()
    print("base url: ", base_url)
    readthread.start(base_url)

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

@app.route('/csvProcessor', methods=['POST'])
@scheduler.task('cron', id='csvProcessor', hour="23", minute='00')
def csvProcessor():
    now = datetime.datetime.now()
    # delta = now + datetime.timedelta(minutes = 1)
    # sleep(15)
    # app.logger.info("Processing CSV FILE - START: {} ".format(now))
    print("Processing CSV FILE - START: {} ".format(now))
    dt = datetime.datetime.now()
    data = {}
    try:
        upload_dates = []
        with open(f'/home/pi/Documents/RFID/failed_uploads.csv', 'r') as failed_uploads: 
            failed = csv.reader(failed_uploads)
            
            for failed_date in failed:
                upload_dates.append(failed_date[0])

            failed_uploads.close()

        with open(f'/home/pi/Documents/RFID/TimeClock/{dt.year}_TimeClock.csv', 'r') as f: 
            csv_reader = csv.DictReader(f)
            line_count = 0
            upload_dates.append(f'{dt.date()}')
            # No failed dates
            for row in csv_reader:
                #print(row)
                # print(dt.date())
                #print(row['date'])
                # yesterday = datetime.datetime.today() - datetime.timedelta(days=2)
                # print(d)
                # if row['date'] == f'{yesterday.date()}':
                # if row['date'] == f'{dt.date()}':
                if row['date'] in upload_dates:
                    data[line_count] = row['date'], row['name'], row['fobid'], row['in/out'], row['time'], row['nolunch']
                    # print(f"\t{row['date']}, {row['name']}, {row['fobid']}, {row['in/out']}, {row['time']}, {row['lunch']}")
                    # line_count += 1
                    line_count += 1
            # print(line_count)
            f.close()

        print("uploading dates: ")
        print(upload_dates)
        data['device'] = getserial()
        data = json.dumps(data)
        print(data)
        headers= {'content-type': 'application/json'}
        res = requests.get(api_url+"processCsv", data=data, headers=headers)
        print("Status Code: ", res.status_code)
        res = json.loads(res.text)
        print("Message: ", res['message'])
        sent_flag = True
        if res['message'] == 'error':
            sent_flag = False
            for i in range(10):
                resx = requests.get(api_url+"processCsv", data=data, headers=headers)
                restxt = json.loads(resx.text)
                if restxt['message'] == 'error':
                    print(resx.status_code)
                    sleep(300)
                    continue
                elif restxt['message'] == "success":
                    sent_flag = True
                    break
                else:
                    sent_flag = True
                    break
        
        #Clears file if sent_flag is true
        if sent_flag:
            print('sent flag')
            f = open(f'/home/pi/Documents/RFID/failed_uploads.csv', "w+")
            f.close()

        #Appends Date if sent_flag is false
        if not sent_flag:
            print("if not sent_flag")
            with open(f'/home/pi/Documents/RFID/failed_uploads.csv', 'a+') as f:
                failed_uploads = csv.writer(f)
                row = [dt]
                failed_uploads.writerow(row)
                f.close()
                

        print("Processing CSV FILE - ENDED: {}".format(now))
        # app.logger.info("Processing CSV FILE - ENDED: {}".format(now))
        # return render_template('index.html')
    except Exception as e:
        print("Processing CSV FILE - FAILED: {}, {}".format(now, e))
        raise
        # return render_template('index.html')

if __name__ == '__main__':
    try:
        # t = threading.Thread(target=start_server)
        # t.daemon = True
        # t.start()
        # startReadThread(True)

        # -------- MAIN
        # readthread.start()
        # -------- MAIN END

        # print("loading fobs")

        # Code Block to check for wifi connection
        # import subprocess
        # ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # try:
        #     output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        #     # print("output:", list(output))
        #     if len(output) != 0:
        #         print(output)
        #         app.logger.info("GETTING FOBS")
        #         loadFobs()
        # except subprocess.CalledProcessError:
        #     # grep did not match any lines
        #     print("No wireless networks connected")
        app.logger.info("GETTING FOBS")
        loadFobs()
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
        