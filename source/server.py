from flask import Flask
from classes import fileclasses
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

#build list of courses from the master course list on server start
mastercoursecsv = fileclasses.csvfile("master_course.csv")
for row in mastercoursecsv.readfrom():
	fileclasses.course.create(row[0],row[1])


#build list of questions from the master question list on server start
masterquestioncsv = fileclasses.csvfile("master_question.csv")
for row in masterquestioncsv.readfrom():
	answers = row[2]
	answers = str(answers).replace(']', "")
	answers = str(answers).replace('[', "")
	#print(answers)
	fileclasses.question.create(row[0],row[1],answers)

#need questions built before surveys so they can be linked into surveys

#build list of surveys from the master survey list on server start
mastersurveycsv = fileclasses.csvfile("master_survey.csv")
for row in mastersurveycsv.readfrom():
	fileclasses.survey.create(row[0],row[1],row[2],row[3],row[4])



def errorMSG(filename,msg):
	print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+msg))
