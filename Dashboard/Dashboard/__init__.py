from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager as manager
from flask_bcrypt import Bcrypt
import json
import os
db = SQLAlchemy()
bcrypt = Bcrypt()

try:
    ##Creates the Flask Application with the configurations -Adrian
    def create_app():
        app = Flask(__name__)

        #DEV
        app.config['SECRET_KEY'] = 'TESTMVLANDSCAPE'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Database13.@localhost/MVLandscape'

        # Prod
        # f = open('/home/mvlandscaping/mysite/config/config.json')
        # obj = json.load(f)
        # f.close()
        # app.config['SECRET_KEY'] = obj['secret_key']
        # app.config['SQLALCHEMY_DATABASE_URI'] = obj['database_uri']
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20

        db.init_app(app)

        #initialized the login manager
        LoginManager = manager()
        LoginManager.login_view = 'auth.login'
        LoginManager.init_app(app)

        #initialized bcrypt
        bcrypt.init_app(app)

        from Landscape.home import home as h_bp
        from Landscape.authenticator import auth as a_bp

        app.register_blueprint(h_bp)
        app.register_blueprint(a_bp)

        from Landscape.database import user_id_query as id_query

        @LoginManager.user_loader
        def load_user(id):
            print("Load User")
            try:
                user = id_query(id)
                return user
            except Exception as e:
                print(e)
                return None
                    
        @LoginManager.unauthorized_handler
        def unauthorized_callback():
            print("Unauthorized Callback")
            return redirect(url_for('home.login'))

        return app
except:
    print(os.getcwd())
    raise
