from flask import Flask
# import threading
# import TimeClock.rfid as RFID
from multiprocessing import Process
from TimeClock.rfid import RFID as RFID
# import webview

try:
    thread = RFID()
    ##Creates the Flask Application with the configurations 
    def create_app():

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret_key'

        from TimeClock.controller import home as h_bp
        from TimeClock.controller import rfid as rfid
        
        app.register_blueprint(h_bp)
        app.register_blueprint(rfid)

        return app

    # print("calling thread target")
    thread.start()

except:
    raise
