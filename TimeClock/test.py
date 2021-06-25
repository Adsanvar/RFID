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
import pyautogui
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
window = webview.create_window("TimeClock", app, fullscreen=True)
# window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
# base_url = "http://localhost:5000/"

base_url = ""
api_url = "http://192.168.1.65:5005/"
read_flag = True

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
            print(text)
            print(repr(text))
            pyautogui.moveTo(512, 300) #moves mouse to center to invoke a wake up rpi if it is sleeping
            val = ""
            if text == None or text  == '':
                val = "Error"
            else:
                # print('\x00' in text)
                if '\x00' in text:
                    val = text.replace('\x00', '')
                else:
                    val = text.rstrip(' ')

            if val == '' or val == None:
                val = "Error"
                payload = {'id': id, 'text': val}
                loadOptions(window, payload)
                # print(window.get_current_url())
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
                payload = {'id': id, 'text': val, 'device': getserial()}
                loadOptions(window, payload)
                # print(window.get_current_url())
                GPIO.output(buzzer,GPIO.HIGH)          
                time.sleep(3)
                GPIO.output(buzzer,GPIO.LOW)
    except:
        print('read exception')
        raise
    finally:
            GPIO.cleanup()

readthread = threading.Thread(target=read)

def write(val):
    try:
        GPIO.cleanup()
        writerx = SimpleMFRC522()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        buzzer = 11
        GPIO.setup(buzzer, GPIO.OUT)
        # text = input('New data:')
        print("Now place your tag to write")
        writerx.write(val)
        print("Written")
    except:
        print('write exception')
        raise
    finally:
            GPIO.cleanup()

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

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
                if (result.isConfirmed) {
                    (async () => {
                                            
                        for(i in result.value)
                        {
                            name = result.value[i].firstname + ' ' +result.value[i].lastname
                            txt = 'Writer'
                            const { value: accept } = await swalWithBootstrapButtons.fire({
                                title: txt,
                                showCancelButton: true,
                                reverseButtons: true,
                                text: `Press \"Continue\" & Place Key On Scanner To Write: ` + name,
                                confirmButtonText: 'Continue',
                                })

                                if (accept) {
                                    let url = '%swriter/' + JSON.stringify(name)
                                    return fetch(url).then(response => {
                                        if (!response.ok) {
                                        throw new Error(response.statusText)
                                        }
                                        Swal.fire('Saved!', '', 'success')
                                    })
                                    .catch(error => {
                                        Swal.showValidationMessage(
                                        `Request failed: ${error}`
                                        )
                                    })
                                    const { value: cont } = await swalBtnOkBootstrap.fire({
                                        title: 'Wrote!',
                                        icon: 'success',
                                        text: `Successfully Wrote: ` + name,
                                        confirmButtonText: 'OK',
                                    })
                                }
                                else
                                {
                                    const { value: cont } = await swalBtnOkBootstrap.fire({
                                        title: 'Cancelled Write',
                                        icon: 'info',
                                        text: name + ': Was not written',
                                        confirmButtonText: 'OK',
                                    })
                                }
                        }
                    })()
            })""" % (payload['text'],payload['id'],payload['text'], payload['device'], base_url, base_url)

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
    return render_template('index.html', read = False)

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
            print(e)
            return jsonify(message='Error')
    else:
        return jsonify(message='Error No Data')

@app.route('/getWrite')
@app.route('/getWrite/<string:data>')
def getWrite(data=None):
    if data != None:
        try:
            headers= {'content-type': 'application/json'}
            res = requests.get(api_url+"getWrite", data=data, headers=headers)
            # print(json.dumps(res.text))
            # global read_flag
            # read_flag = False
            # window.load_url(base_url+"writer/"+res.text)
            # stopReadThread()
            # print(res.text)
            return res.text
        except Exception as e:
            print(e)
            return jsonify(message='Error')
    else:
        return jsonify(message='Error No Data')

@app.route('/writer')
@app.route('/writer/<string:data>')
def writer(data=None):
    print(data)
    if data != None:
        print("in data not empty")
        try:
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
            global read_flag
            read_flag = False
            stopReadThread()
            print("rendering")
            return render_template('writer.html', data=data)
        except Exception as e:
            print(e)
            print("in exception")
            return jsonify(message='Error')
    else:
        print("no data")
        return jsonify(message='Error No Data')


def setBaseUrl():
    global base_url
    base_url = window.get_current_url()
    print("base url: ", base_url)

def stopReadThread():
    readthread._stop_event.set()

def startReadThread():
    readthread._stop_event = threading.Event()
    readthread.daemon = True
    readthread.start()

if __name__ == '__main__':

    # t = threading.Thread(target=start_server)
    # t.daemon = True
    # t.start()
    startReadThread()
    # webview.start(setBaseUrl, debug=True)
    webview.start(setBaseUrl)
    sys.exit()