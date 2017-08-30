import csv
from flask import Flask, redirect, render_template, request, url_for
from server import app, users
import time

authenticated = 0

@app.route("/", methods=["GET", "POST"])
def index():
	global authenticated
	authenticated = 0
	if request.method == "POST":

		user = request.form["username"]
		pwd = request.form["password"]

		# Check Password

		if check_password(user,pwd):
			
			print("Valid password")
			authenticated = 1
			return redirect(url_for("home"))

		else:

			print("Invalid Password") #tmp

			return render_template("index.html", invalid=True)

	return render_template("index.html", invalid=False)


def check_password(user, pwd):

	#if you dont use .get to look inside the dictionary
	#you will get errors if the username is not there
	#.get will return none which is seen as false by the statement

	if pwd == users.get(user):
		return True
	else:
		return False

@app.route("/home",methods=["GET", "POST"])
def home():
	# button to go to questions
	# button to go to surveys
	global authenticated
	if request.method == "POST":
	   if "createsvy" in request.form:
		   return redirect(url_for("createsurvey"))

	if (authenticated):
		return render_template("home.html")
	else:
		return redirect(url_for("index"))


@app.route("/createsurvey",methods=["GET", "POST"])
def createsurvey():
	if request.method == "POST":
		survey_name = request.form["svyname"]
		survey_course = request.form["svycourse"]
		survey_date = time.strftime("%d/%m/%Y,%I:%M:%S")
		ID = textfile("surveyID.txt")
		survey_ID = ID.updateID()
		mastercsv = csvfile("mastersurvey.csv")
		mastercsv.writeto(survey_ID,survey_name,survey_course,survey_date)

	return render_template("createsvy.html")


class IDfile():
	def __init__(self,filename):
		self._name = filename

class textfile(IDfile):
	def getcurrentID(self):
		fileID = open(self._name,"r+")
		val = fileID.read()
		if val == "":
			return 0
		fileID.close()
		return str(val)
	def updateID(self):
		new_val = int(self.getcurrentID())
		IDfile = open(self._name,"w")
		new_val += 1
		IDfile.write(str(new_val))
		return str(new_val)

class csvfile(IDfile):
	def writeto(self,ID,name,course,time):
		with open(self._name,'a') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([ID,name,course,time])
	def readfrom(self):
		with open(self._name,'r') as csv_in:
			reader = csv.reader(csv_in)
			namelist = []
			for row in reader:
				namelist.append(row)
			return namelist
