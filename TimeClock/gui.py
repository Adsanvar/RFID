import json
import os
import requests

def validateFob(payload, api_url):
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
    elif validateFob(payload, api_url):
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