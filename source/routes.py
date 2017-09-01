import csv, ast, os, time
from flask import Flask, redirect, render_template, request, url_for
from server import app, users, authenticated
from functions import append
from classes import fileclasses

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

	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))

	if request.method == "POST":
		survey_name = request.form["svyname"]
		survey_course = request.form["svycourse"]
		survey_date = time.strftime("%d/%m/%Y,%I:%M:%S")
		ID = fileclasses.textfile("surveyID.txt")
		survey_ID = ID.updateID()
		mastercsv = fileclasses.csvfile("mastersurvey.csv")
		mastercsv.writeto(survey_ID, survey_name, survey_course, survey_date)

	return render_template("createsurvey.html")

@app.route("/createquestion", methods=["GET", "POST"])
def createquestion():

	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))
	
	if request.method == "POST":

		#TODO:	implement method to add any number of answers to a question
		# 		possibly use a dict, and add answer button that polls server
		# 		storing each answer, until final submission submitted

		question = request.form["question"]
		answer_one = request.form["option_one"]
		answer_two = request.form["option_two"]
		answer_three = request.form["option_three"]
		answer_four = request.form["option_four"]

		survey = -1

		append.question(survey, question, [answer_one,answer_two,answer_three,answer_four])

	return render_template("createquestion.html")


