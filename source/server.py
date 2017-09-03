from flask import Flask
from classes import fileclasses


app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"


users = {"admin": "password"}
authenticated = 0


#build list of questions from the master question list on server start
masterquestioncsv = fileclasses.csvfile("master_question.csv")
for row in masterquestioncsv.readfrom():
	test = row[2:]
	test = str(test).replace(']', "")
	test = str(test).replace('[', "")
	fileclasses.question.create(row[0],row[1],test)

#need questions built before surveys so they can be linked into surveys

#build list of surveys from the master survey list on server start
mastersurveycsv = fileclasses.csvfile("master_survey.csv")
for row in mastersurveycsv.readfrom():
	fileclasses.survey.create(row[0],row[1],row[2],row[3],row[4])



def errorMSG(filename,msg):
	print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+msg))
