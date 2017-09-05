import csv, ast, os, time, copy
from flask import Flask, redirect, render_template, request, url_for,flash
from server import app, users, authenticated,errorMSG
from functions import append, get
from classes import fileclasses
from defines import masterSurveys, masterQuestions

_authenticated = authenticated

@app.route("/")
def index():
	global _authenticated
	survey_pool = fileclasses.survey.read_all()

	return render_template("home.html", survey_pool=survey_pool, authenticated=_authenticated)


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

		if (get.cleanString(str(survey_name))):
			if (survey_name == "" or survey_course == "" or survey_date == "" or survey_questions == []):
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
		else:
			errorMSG("routes.createsurvey","Invalid characters in Survey Name")

	#Populate Question and Course lists
	questions_pool = fileclasses.question.list()
	course_list = fileclasses.course.readall()

	return render_template("createsurvey.html",questions_pool=questions_pool,course_list = course_list)



@app.route("/createquestion", methods=["GET", "POST"])
def createquestion():

	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))

	if request.method == "POST":

		#TODO:	implement method to add any number of answers to a question
		# 		possibly use a dict, and add answer button that polls server
		# 		storing each answer, until final submission submitted

		#TODO: Display Error to user adding question if they forget fields

		question = request.form["question"]
		answer_one = request.form["option_one"]
		answer_two = request.form["option_two"]
		answer_three = request.form["option_three"]
		answer_four = request.form["option_four"]

		answers = [answer_one,answer_two,answer_three,answer_four]
		answers = list(filter(None, answers))

		#if only one answer provided then return with error msg (this is not a valid question)
		if(len(answers)<2):
			questions_pool = fileclasses.question.list()
			return render_template("createquestion.html",questions_pool=questions_pool)

		if(question==""):
			questions_pool = fileclasses.question.list()
			errorMSG("append.question","No Question Provided")
			return render_template("createquestion.html",questions_pool=questions_pool)

		#check for invalid characters

		validStrings = copy.copy(answers)
		validStrings.append(question)

		for text in validStrings:
			if (get.cleanString(str(text))==False):
				questions_pool = fileclasses.question.list()
				errorMSG("routes.createsurvey","Invalid input in fields")
				questions_pool = fileclasses.question.list()
				return render_template("createquestion.html",questions_pool=questions_pool)


		ID = fileclasses.textfile("questionID.txt")
		qID = ID.updateID()

		if(qID==""):
			questions_pool = fileclasses.question.list()
			errorMSG("append.question","No qID Issued")
			return render_template("createquestion.html",questions_pool=questions_pool)

		#update master csv file & survey class
		answercsv = fileclasses.csvfile("master_question.csv")
		answercsv.master_question(qID, question, str(answers))

		#Update Question Pool
		questions_pool = fileclasses.question.list()

		return render_template("createquestion.html",questions_pool=questions_pool)

	else:

		questions_pool = fileclasses.question.list()
		return render_template("createquestion.html",questions_pool=questions_pool)


@app.route('/<int:sID>',methods=["GET", "POST"])
def complete_survey(sID):

	if request.method == "GET":
		#see if it is a valid survey
		#if not then return to homepage with error msg?

		#atm it goes to a bad request page if not all checkboxes filled out

		questionList = get.questionList(sID)

		#print("getrequest:",questionList)

		if questionList != []:
			return render_template('answersurvey.html',questionList=questionList, surveyID=sID)

		else:
			#not a valid survey link
			return redirect(url_for("home"))
	else:

		#append answers to answer sheet
		questionList = get.questionList(sID)
		answersList = []

		for qID in questionList:
			answer = request.form[qID[0]]
			filename = str(sID)+".csv"
			answercsv = fileclasses.csvfile(filename)
			answercsv.appendfield(str(qID[0]),"answers",str(answer))

		return redirect(url_for("submit"))