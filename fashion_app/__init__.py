from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES ,UploadSet, configure_uploads 
import os
from flask import Flask



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key =  '60febe5575281e2b2efebb36'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fashion_market'
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(basedir ,"/home/drkimpatrick/Desktop/my_add/fashion_app/images")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024




photos = UploadSet('photos',IMAGES)        
configure_uploads(app,photos)           



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

    
                                      
from fashion_app import routes

