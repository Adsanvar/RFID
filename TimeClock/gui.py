import json
import os
import requests

success_flag = False
fobs = None

# def validateFob(payload, api_url):
#     try:
#         headers= {'content-type': 'application/json'}
#         data = json.dumps(payload)
#         res = requests.get(api_url+"validateFob", data=data, headers=headers)
#         res = json.loads(res.text)
#         if res['message']:
#             return True
#         else:
#             return False
#     except Exception as e:
#         print('Exception in /validateFob')
#         print(e)
#         return False


def validateFob(payload):

    with open('/home/pi/Documents/rfid/fobs.json', 'r', encoding='utf-8') as f:
        fobs = json.load(f)
    
    print(fobs)
    print(payload)
    for o in fobs:
        # print(type(o['fobid']))
        # print(type(payload['id']))
        if int(o['fobid']) == payload['id']:
            print("fobid matched payload id")
            if o['text'] == payload['text']:
                print("text matched payload text")
                return True
            else:
                return False


def sendWriteRequest(payload, api_url):
    headers= {'content-type': 'application/json'}
    res = requests.get(api_url+"writeFob", data=json.dumps(payload), headers=headers)
    val = json.loads(res.text)
    val = val['message']
    global success_flag
    if val == 'success':
        print("server success, setting success flag to True")
        # flash(val, val) # 'success', 'success'
        # return redirect(url_for('getWrite', data = payload))
        success_flag = True
    else:
        # flash(val, val) # 'error', 'error'
        print('server failure, setting success flag to False')
        success_flag = False

def loadOptions(window, payload, base_url, api_url):
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
        return False
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
            allowOutsideClick: false,
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
            /*allowOutsideClick: () => !swalWithBootstrapButtons.isLoading(),*/
            }).then((result) => {
                /*Might Not Need Code Here*/
                if(result.dismiss === Swal.DismissReason.cancel)
                {
                    let url = '%sresumeRead'
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
                }
            })""" % (payload['text'],payload['id'],payload['text'], payload['device'], base_url, base_url)

            window.evaluate_js(tmp)
            return True
        else:
            tmp = """ const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: 'btn-clock-in margin',
                denyButton: 'btn-clock-out margin',
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
            confirmButtonText: 'Entrada',
            showDenyButton: true,
            denyButtonText: 'Salida',
            showCancelButton: true,
            cancelButtonText: 'Horas',
            width: 600,
            timer: 60000,
            footer: "Seleccionar Opción o Oprime Afuera De Este Modulo Para Cerrar.",
            html:
                '<hr/>'+
                '<a href="/getHours/%s">Horas</a>'+
                '<input id="id" class="swal2-input" value="%s" type="hidden">' +
                '<input id="name" class="swal2-input" value="%s" type="hidden">',
            preConfirm: () => {
                id = document.getElementById('id').value
                name = document.getElementById('name').value
                data = {'id': id, 'text': name}
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
                } else if (result.isDenied) 
                {   
                    swalBtnOkBootstrap.fire({
                                title: '%s',
                                confirmButtonText: 'OK',
                                icon: 'info',
                                width: 600,
                                allowOutsideClick: false,
                                html:
                                    `
                                    <input id="id" class="swal2-input" value="%s" type="hidden">
                                    <input id="name" class="swal2-input" value="%s" type="hidden">
                                    <div class="big margin">
                                        <input type="checkbox" name="lunch-cbx" id="lunch-cbx" /> 
                                        <label for="lunch-cbx">Selecciona Aqui Si No Tomaste Almuerzo</label>
                                    </div>
                                    <hr/>`,
                                preConfirm: () => {
                                    id = document.getElementById('id').value
                                    name = document.getElementById('name').value
                                    lunch = document.getElementById('lunch-cbx').checked
                                    data = {'id': id, 'text': name, 'lunch':lunch}
                                    let url = '%sclockout/' + JSON.stringify(data)
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
                                }).then((resultx) => {
                                    if (resultx.isConfirmed) {
                                        if (resultx.value.message === 'Success')
                                        {
                                            swalBtnOkBootstrap.fire({
                                            icon: 'success',
                                            title: 'Todo Listo!',
                                            timer: 5000,
                                            })
                                        }
                                    }
                                })
                }
                else if(result.dismiss === Swal.DismissReason.cancel)
                {
                    let url = '%sgetHours/%s'
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
                }
                
            })""" % (payload['text'], payload['id'], payload['text'], base_url, payload['text'], payload['id'], payload['text'], base_url, base_url, payload['id'] )

            window.evaluate_js(tmp)
            return True
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
        return False