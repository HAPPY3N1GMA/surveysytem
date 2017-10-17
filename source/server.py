from flask import Flask
from flask_login import LoginManager
from models import UniUser, Admin, Staff, Student, Guest



app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"


#  flask login config - to be moved to login-cfg.py later
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
	user = UniUser.query.get(userid)
	Role = eval(user.role)
	return Role.query.get(userid)


def errorMSG(filename="",msg="",other=""):
	print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+str(msg)+str(other)))
