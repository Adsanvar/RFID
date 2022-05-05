# from flask import Flask
# # import threading
# # import TimeClock.rfid as RFID
# # from TimeClock.rfid import RFID as RFID

# try:
#     # thread = RFID()
#     ##Creates the Flask Application with the configurations 
#     def create_app():

#         app = Flask(__name__)
#         app.config['SECRET_KEY'] = 'test_secret_key'

#         from TimeClock.controller import home as h_bp
#         # from TimeClock.rfid import rf as rfid
        
#         app.register_blueprint(h_bp)
#         # app.register_blueprint(rfid)

#         return app
#     # print("calling thread target")
#     # thread.start()

# except:
#     raise

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os

db = SQLAlchemy()

try:
    def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'TESTMVLANDSCAPE'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Database13.@localhost/mvdb'
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

        from TimeClock.home import home as h_bp
        app.register_blueprint(h_bp)
        
        h_bp.create()

        return app
except:
    raise

