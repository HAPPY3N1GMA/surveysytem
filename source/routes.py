import csv, ast, os, time
from flask import Flask, redirect, render_template, request, url_for,flash
from server import app, users, authenticated,errorMSG
from functions import append, get
from classes import fileclasses
from defines import masterSurveys, masterQuestions

_authenticated = authenticated
_masterSurveys = masterSurveys
_masterQuestions = masterQuestions

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


@app.route("/submitted")
def submit(): 
	return render_template("completed.html")

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
		survey_name = str(survey_name)
		survey_course = request.form["svycourse"]
		survey_date = time.strftime("%d/%m/%Y,%I:%M:%S")
		survey_questions = request.form.getlist('question')
		print(survey_questions)
		if (survey_name == "" or survey_course == "" or survey_date == ""):
			errorMSG("routes.createsurvey","Invalid input in fields")
		else:
			ID = fileclasses.textfile("surveyID.txt")
			survey_ID = ID.updateID()
			mastercsv = fileclasses.csvfile("master_survey.csv")
			mastercsv.writeto(survey_ID, survey_name, survey_course, survey_date,list(survey_questions))
			flash("{}".format(survey_ID))

			#create survey answers page template
			answercsv = fileclasses.csvfile(str(survey_ID)+".csv")
			answercsv.buildanswer(survey_questions)


	questions_pool = fileclasses.question.readall()

	course_list = fileclasses.course.readall()
	#print(courses)

	#courses = fileclasses.csvfile("courses.csv")
	#course_list = courses.readfrom()

	return render_template("createsurvey.html",questions_pool=questions_pool,course_list = course_list)

@app.route("/createquestion", methods=["GET", "POST"])
def createquestion():

	global _authenticated, _masterQuestions
	if not _authenticated:
		return redirect(url_for("login"))

	if request.method == "POST":

		#TODO:	implement method to add any number of answers to a question
		# 		possibly use a dict, and add answer button that polls server
		# 		storing each answer, until final submission submitted

		#TODO: Display Error to user adding question if they forget fields

		#old method using csv file each time - now redundant using classes
		#mastercsv = fileclasses.csvfile("master_question.csv")
		#questions_pool = mastercsv.readfrom()
		questions_pool = fileclasses.question.readall()

		question = request.form["question"]
		answer_one = request.form["option_one"]
		answer_two = request.form["option_two"]
		answer_three = request.form["option_three"]
		answer_four = request.form["option_four"]

		survey = -1

		answers = [answer_one,answer_two,answer_three,answer_four]
		answers = list(filter(None, answers))

		#if only one answer provided then return with error msg (this is not a valid question)
		if(len(answers)<2):
			return render_template("createquestion.html",questions_pool=questions_pool)

		append.question(survey, question, str(answers))

		questions_pool = fileclasses.question.readall()

		return render_template("createquestion.html",questions_pool=questions_pool)

	else:
		#old method using csv file each time - now redundant using classes
		#mastercsv = fileclasses.csvfile("master_question.csv")
		#questions_pool = mastercsv.readfrom()

		questions_pool = fileclasses.question.readall()
		return render_template("createquestion.html",questions_pool=questions_pool)


@app.route('/<int:sID>',methods=["GET", "POST"])
def complete_survey(sID):

	if request.method == "GET":
		#see if it is a valid survey
		#if not then return to homepage with error msg?

		#atm it goes to a bad request page if not all checkboxes filled out

		questionList = get.questionList(sID)

		print("getrequest:",questionList)

		if questionList != []:
			return render_template('answersurvey.html',questionList=questionList, surveyID=sID)

		else:
			#not a valid survey link
			#print("TEST1")
			return redirect(url_for("home"))
	else:
		#append answers to answer sheet
		questionList = get.questionList(sID)
		answersList = [];
		for qID in questionList:
			answer = request.form[qID[0]]
			filename = str(sID)+".csv"
			answercsv = fileclasses.csvfile(filename)
			answercsv.appendfield(str(qID[0]),"answers",str(answer))

		return redirect(url_for("submit"))