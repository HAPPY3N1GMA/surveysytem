from flask import Flask
from flask_login import LoginManager
from models import users_model, surveys_model
import schedule
import time
import _thread
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base





app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"


#  flask login config - to be moved to login-cfg.py later
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
	return users_model.UniUser.query.get(userid)


