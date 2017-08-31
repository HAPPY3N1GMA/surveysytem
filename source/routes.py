import csv, ast, os, time
from flask import Flask, redirect, render_template, request, url_for
from server import app, users, authenticated
from functions import append

_authenticated = authenticated


@app.route("/", methods=["GET", "POST"])
def index():
	# button to go to questions
	# button to go to surveys
	return render_template("home.html")


@app.route("/admin")
def admin(): 
	global _authenticated
	if _authenticated:
		# read csv data into a list
		return render_template("admin.html")
	else:
		return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
	global _authenticated
	if request.method == "POST":

		user = request.form["username"]
		pwd = request.form["password"]

		# Check Password
		if check_password(user, pwd):
			
			print("Valid password")
			_authenticated = 1
			return redirect(url_for("admin"))

		else:
			return render_template("login.html", invalid=True)

	return render_template("login.html", invalid=False)


def check_password(user, pwd):

	# if you dont use .get to look inside the dictionary
	# you will get errors if the username is not there
	# .get will return none which is seen as false by the statement

	if pwd == users.get(user):
		return True
	else:
		return False


@app.route("/home")
def home():
		return redirect(url_for("index"))


@app.route("/createsurvey", methods=["GET", "POST"])
def createsurvey():
	if request.method == "POST":
		survey_name = request.form["svyname"]
		survey_course = request.form["svycourse"]
		survey_date = time.strftime("%d/%m/%Y,%I:%M:%S")
		ID = textfile("surveyID.txt")
		survey_ID = ID.updateID()
		mastercsv = csvfile("mastersurvey.csv")
		mastercsv.writeto(survey_ID, survey_name, survey_course, survey_date)

	return render_template("createsurvey.html")

@app.route("/createquestion", methods=["GET", "POST"])
def createquestion():
	# if request.method == "POST":
		# TO DO: Add new question creation

	return render_template("createquestion.html")


class IDfile():
	def __init__(self, filename):
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
