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
db = SQLAlchemy()

try:
    ##Creates the Flask Application with the configurations -Adrian
    def create_app():
        app = Flask(__name__)

        # Prod
        # f = open('/home/mvlandscaping/mysite/config/config.json')
        # obj = json.load(f)
        # f.close()
        # app.config['SECRET_KEY'] = obj['secret_key']
        # app.config['SQLALCHEMY_DATABASE_URI'] = obj['database_uri']
        # DEV
        app.config['SECRET_KEY'] = "TEST_SECRET_KEY"
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MVTech3.@localhost/mvdb'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299


        db.init_app(app)

        from api.home import home as h_bp

        app.register_blueprint(h_bp)
        return app
except:
    print(os.getcwd())
    raise


