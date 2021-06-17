from flask import Flask
import threading
import TimeClock.rfid as RFID
from multiprocessing import Process

try:
    ##Creates the Flask Application with the configurations 
    def create_app():

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret_key'

        from TimeClock.controller import home as h_bp
        app.register_blueprint(h_bp)

        return app

    p = Process(target=RFID.read())
    # p.daemon = True
    p.start() 
    # read()
    # def read():
    #     x = threading.Thread(target=RFID.read())
    #     x.start()
except:
    raise
