from flask import Flask
from flask_login import LoginManager
from models import UniUser



app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"


users = {"admin": "password"}
authenticated = 0

#  flask login config - to be moved to login-cfg.py later
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
	return UniUser.query.get(userid)


def errorMSG(filename,msg):
	print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+msg))
