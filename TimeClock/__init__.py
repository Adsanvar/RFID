from flask import Flask
# import threading
# import TimeClock.rfid as RFID
from multiprocessing import Process
from TimeClock.rfid import RFID as RFID

try:
    ##Creates the Flask Application with the configurations 
    def create_app():

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret_key'

        from TimeClock.controller import home as h_bp
        app.register_blueprint(h_bp)

        return app
    thread = RFID()
    p = Process(target=thread.start())
    # p.daemon = True
    p.start() 
    # read()
    # def read():
    #     x = threading.Thread(target=RFID.read())
    #     x.start()
except:
    raise
