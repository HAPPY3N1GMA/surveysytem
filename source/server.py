from flask import Flask
from classes import fileclasses


app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"


users = {"admin": "password"}
authenticated = 0




#build list of surveys from the master list on server start
mastercsv = fileclasses.csvfile("master_survey.csv")
for row in mastercsv.readfrom():
	fileclasses.survey.create(row[0],row[1],row[2],row[3],row[4])



def errorMSG(filename,msg):
	print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+msg))
