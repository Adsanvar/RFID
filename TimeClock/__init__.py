from flask import Flask
import threading
import TimeClock.rfid as RFID

try:
    ##Creates the Flask Application with the configurations 
    def create_app():

        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret_key'

        from TimeClock.controller import home as h_bp
        app.register_blueprint(h_bp)

        return app
    
    def read():
        x = threading.Thread(target=RFID.read(), daemon=True)
        x.start()
    
    read()
    
except:
    raise
