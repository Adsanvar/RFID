from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for, current_app
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

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
window = webview.create_window("TimeClock", app, fullscreen=True)
# window = webview.create_window("TimeClock", "http://localhost:5000/", fullscreen=True)
# base_url = "http://localhost:5000/"

base_url = ""

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
            pyautogui.moveTo(512, 300, duration = 1) #moves mouse to center to invoke a wake up rpi if it is sleeping
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
                payload = {'id': id, 'text': val}
                loadOptions(window, payload)
                # print(window.get_current_url())
                GPIO.output(buzzer,GPIO.HIGH)          
                time.sleep(5)
                GPIO.output(buzzer,GPIO.LOW)
    except:
        raise
    finally:
            GPIO.cleanup()

def loadOptions(window, payload):
    # url = base_url + json.dumps(payload)
    # print("URL: ", url)

    tmp2 = """ const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
        confirmButton: 'btn-clock-in',
        cancelButton: 'btn-clock-out'
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
    text: "Seleccionar Opción",
    confirmButtonText: 'Entrada',
    showCancelButton: true,
    cancelButtonText: 'Salida',
    html:
        '<input id="id" class="swal2-input" value="%s" type="hidden">' +
        '<input id="name" class="swal2-input" value="%s" type="hidden">',
    /*width: 600,*/
    }).then((result) => {
    if (result.isConfirmed) {
        swalBtnOkBootstrap.fire({
        icon: 'success',
        title: 'Todo Listo!',
        timer: 4000,
        })
    } else if ( result.dismiss === Swal.DismissReason.cancel) 
    {   
        id = document.getElementById('id').value
        name = document.getElementById('name').value
        swalBtnOkBootstrap.fire(
        {
            title: name,
            html: `
            <div class="big">
                <input type="checkbox" name="no-lunch-cbx" id="no-lunch-cbx" /> 
                <label for="no-lunch-cbx">Sin Almuerzo</label>
            </div>
            `,
            width: 600,
        })
    }
    })""" % (payload['text'], payload['id'], payload['text'])

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
    else:
        
        window.evaluate_js(tmp2)
    # string = 'Swal.fire({title: \'Do you want to save the changes?\', showDenyButton: true, showCancelButton: true, confirmButtonText: \'Entrada\', denyButtonText: \'Cancel\',}).then((result) => { if (result.isConfirmed) { Swal.fire(\'Saved!\', \'\', \'success\')} else if (result.isDenied) {Swal.fire(\'Changes are not saved\', \'\', \'info\')}})'
    # window.evaluate_js('Swal.fire({ position: \'center\', icon: \'success\', title: \'Your work has been saved\', showConfirmButton: false, timer: 1500 })')
    # window.evaluate_js("Swal.fire({ title: 'Do you want to save the changes?', showDenyButton: true, showCancelButton: true, confirmButtonText: `Save`, denyButtonText: `Don't save`, }).then((result) => { if (result.isConfirmed) { Swal.fire('Saved!', '', 'success') } else if (result.isDenied) { Swal.fire('Changes are not saved', '', 'info') })")
    string = """
    const { value: formValues } = await Swal.fire({
    title: 'Multiple inputs',
    html:
        '<input id="swal-input1" class="swal2-input">' +
        '<input id="swal-input2" class="swal2-input">',
    preConfirm: () => {
        return [
        document.getElementById('swal-input1').value,
        document.getElementById('swal-input2').value
        ]
    }
    })
    if (formValues) {
    Swal.fire(JSON.stringify(formValues))
    }"""
    # window.evaluate_js(string)
    # window.load_url(url)

# def start_server():
#     # app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
#     app.run(host='0.0.0.0', port=5000)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:data>', methods=['GET', 'POST'])
def index(data=None):
    if data != None:
        data = json.loads(data)
        print(data)
        if data['text'] == 'Error':
            flash("Error Leyendo Etiqueta", 'error')
            return render_template('index.html', read = False)
        else:
            return render_template('index.html', read = True, data = data['text'] )
    else:
        return render_template('index.html', read = False)

def setBaseUrl():
    global base_url
    base_url = window.get_current_url()
    print("base url: ", base_url)

if __name__ == '__main__':

    # t = threading.Thread(target=start_server)
    # t.daemon = True
    # t.start()

    r = threading.Thread(target=read)
    r.daemon = True
    r.start()

    # webview.start(setBaseUrl, debug=True)
    webview.start(setBaseUrl)
    sys.exit()