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
from TimeClock.reader import Reader

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
window = webview.create_window("TimeClock", app, fullscreen=True)
# window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
# base_url = "http://localhost:5000/"

base_url = ""
api_url = "http://192.168.1.65:5005/"

readthread = Reader(window = window)


# read_flag = True

# def read():
#     try:
#         reader = SimpleMFRC522()
#         GPIO.setwarnings(False)
#         GPIO.setmode(GPIO.BOARD)
#         buzzer = 11
#         GPIO.setup(buzzer, GPIO.OUT)
#         print("in run.")
#         while read_flag:
#             print("Ready For Next")
#             id, text = reader.read()
#             if read_flag:
#                 print(id)
#                 print(text)
#                 print(repr(text))
#                 pyautogui.moveTo(512, 300) #moves mouse to center to invoke a wake up rpi if it is sleeping
#                 val = ""
#                 if text == None or text  == '':
#                     val = "Error"
#                 else:
#                     # print('\x00' in text)
#                     if '\x00' in text:
#                         val = text.replace('\x00', '')
#                     else:
#                         val = text.rstrip(' ')

#                 if val == '' or val == None:
#                     val = "Error"
#                     payload = {'id': id, 'text': val}
#                     loadOptions(window, payload)
#                     # print(window.get_current_url())
#                     GPIO.output(buzzer,GPIO.HIGH)              
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.LOW)            
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.HIGH)
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.LOW)
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.HIGH)
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.LOW)
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.HIGH)
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.LOW)
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.HIGH)
#                     time.sleep(.5)
#                     GPIO.output(buzzer,GPIO.LOW)
#                 else:
#                     payload = {'id': id, 'text': val, 'device': getserial()}
#                     loadOptions(window, payload)
#                     # print(window.get_current_url())
#                     GPIO.output(buzzer,GPIO.HIGH)          
#                     time.sleep(3)
#                     GPIO.output(buzzer,GPIO.LOW)
#             else:
#                 GPIO.cleanup()
#     except:
#         print('read exception')
#         raise
#     finally:
#             GPIO.cleanup()

# readthread = threading.Thread(target=read)
# writethread = threading.Thread()

# def write(val, employeeId):
#     try:
#         global readthread
#         global writethread
#         if readthread.is_alive():
#             stopReadThread()
#         else:
#             GPIO.cleanup()
#             readerx = SimpleMFRC522()
#             print("Scan To Read, readeropen?: ", readthread.is_alive())
#             print("Scan To Read, writeropen?: ", writethread.is_alive())
#             id, text = readerx.read()
#             GPIO.cleanup()        
#             writerx = SimpleMFRC522()
#             flash("Place ID to Write", 'success')
#             print("Now place your tag to write")
#             writerx.write(val)
#             GPIO.setwarnings(False)
#             GPIO.setmode(GPIO.BOARD)
#             buzzer = 11
#             GPIO.setup(buzzer, GPIO.OUT)
#             GPIO.output(buzzer,GPIO.HIGH)
#             time.sleep(2)
#             GPIO.output(buzzer,GPIO.LOW)
#             print("Written")
#             flash("Written", 'success')
#             payload = {'id': id, 'text': val, 'device': getserial(), 'employeeId': employeeId}
#             sendWriteRequest(payload)
#     except:
#         print('write exception')
#         raise
#     finally:
#             GPIO.cleanup()

def sendWriteRequest(payload):
    headers= {'content-type': 'application/json'}
    res = requests.get(api_url+"writeFob", data=json.dumps(payload), headers=headers)
    flash(res.text, 'success')

def validateFob(payload):
    try:
        headers= {'content-type': 'application/json'}
        data = json.dumps(payload)
        res = requests.get(api_url+"validateFob", data=data, headers=headers)
        res = json.loads(res.text)
        if res['message']:
            return True
        else:
            return False
    except Exception as e:
        print('Exception in /validateFob')
        print(e)
        return False

def loadOptions(window, payload):
    # url = base_url + json.dumps(payload)
    # print("URL: ", url)
    if payload['text'] == 'Error':
        string = """
        const swalBtnOkBootstrap = Swal.mixin({
        customClass: {
            confirmButton: 'btn-ok',
        },
        buttonsStyling: false
        })
        
        swalBtnOkBootstrap.fire({
        icon: 'error',
        title: 'Error Leyendo Etiqueta!',
        timer: 4000,
        })"""
        window.evaluate_js(string)
    elif validateFob(payload):
        if payload['text'] == 'Admin':
            tmp = """ const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: 'btn-clock-in margin',
                cancelButton: 'btn-cancel margin'
            },
            buttonsStyling: false
            })

            const swalBtnOkBootstrap = Swal.mixin({
            customClass: {
                confirmButton: 'btn-ok',
            },
            buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
            title: '%s',
            confirmButtonText: 'Write',
            showCancelButton: true,
            cancelButtonText: 'Cancel',
            width: 600,
            timer: 60000,
            closeOnCancel: true,
            html:
                '<hr/>',
            preConfirm: () => {
                data = {'id': '%s', 'text': '%s', 'device': '%s'}
                let url = '%sgetWrite/'+ JSON.stringify(data)
                return fetch(url).then(response => {
                    if (!response.ok) {
                    throw new Error(response.statusText)
                    }
                    return response.json()
                })
                .catch(error => {
                    Swal.showValidationMessage(
                    `Request failed: ${error}`
                    )
                })
            },
            allowOutsideClick: () => !swalWithBootstrapButtons.isLoading(),
            }).then((result) => {
                /*Might Not Need Code Here*/
            })""" % (payload['text'],payload['id'],payload['text'], payload['device'], base_url)

            window.evaluate_js(tmp)
        else:
            tmp = """ const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: 'btn-clock-in margin',
                cancelButton: 'btn-clock-out margin'
            },
            buttonsStyling: false
            })

            const swalBtnOkBootstrap = Swal.mixin({
            customClass: {
                confirmButton: 'btn-ok',
            },
            buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
            title: '%s',
            
            confirmButtonText: 'Entrada',
            showCancelButton: true,
            cancelButtonText: 'Salida',
            width: 600,
            timer: 60000,
            footer: "Seleccionar Opción o Oprime Afuera De Este Modulo Para Cerrar.",
            html:
                '<hr/>'+
                '<input id="id" class="swal2-input" value="%s" type="hidden">' +
                '<input id="name" class="swal2-input" value="%s" type="hidden">',
            preConfirm: () => {
                id = document.getElementById('id').value
                name = document.getElementById('name').value
                data = {'id': id, 'text': name, 'device': '%s'}
                let url = '%sclockin/' + JSON.stringify(data)
                return fetch(url).then(response => {
                    if (!response.ok) {
                    throw new Error(response.statusText)
                    }
                    return response.json()
                })
                .catch(error => {
                    Swal.showValidationMessage(
                    `Request failed: ${error}`
                    )
                })
            },
            allowOutsideClick: () => !Swal.isLoading(),
            }).then((result) => {
            if (result.isConfirmed) {
                if (result.value.message === 'Success')
                {
                    swalBtnOkBootstrap.fire({
                    icon: 'success',
                    title: 'Todo Listo!',
                    timer: 5000,
                    })
                }else
                {
                    swalBtnOkBootstrap.fire({
                    icon: 'error',
                    title: 'Error',
                    text: '${result.value.message}',
                    timer: 10000,
                    })
                }
            } else if ( result.dismiss === Swal.DismissReason.cancel) 
            {   
                id = document.getElementById('id').value
                name = document.getElementById('name').value
                swalBtnOkBootstrap.fire(
                {
                    title: name,
                    icon: 'info',
                    showLoaderOnConfirm: true,
                    html: `
                    <div class="big margin">
                        <input type="checkbox" name="no-lunch-cbx" id="no-lunch-cbx" /> 
                        <label for="no-lunch-cbx">Selecciona Aqui Si No Tomaste Almuerzo</label>
                    </div>
                    <hr/>
                    `,
                    width: 600,
                })
            }
            })""" % (payload['text'], payload['id'], payload['text'], payload['device'], base_url)

            window.evaluate_js(tmp)
    else:
        string = """
        const swalBtnOkBootstrap = Swal.mixin({
        customClass: {
            confirmButton: 'btn-ok',
        },
        buttonsStyling: false
        })
        
        swalBtnOkBootstrap.fire({
        icon: 'error',
        title: 'Error, No Pude Validar Tu Llave',
        timer: 10000,
        })"""
        window.evaluate_js(string)

    # window.load_url(url)

# def start_server():
#     # app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
#     app.run(host='192.168.1.79', port=5000)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'exitWrite' in request.form:
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