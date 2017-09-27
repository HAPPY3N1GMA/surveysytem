import csv, ast, os, time, copy, datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, users, authenticated,errorMSG
from functions import append, get
from classes import fileclasses
from defines import masterSurveys, masterQuestions, debug
from models import GeneralQuestion, MCQuestion, SurveyResponse, QuestionResponse
from models import Survey, Course, UniUser
from database import db_session, Base

#got tired of logging in password each time
if(debug):
	_authenticated = authenticated
else:
	_authenticated = True


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


@app.route("/dbtest")
def db_test():
	# u = GeneralQuestion('How high are you?')
	# db_session.add(u)
	# db_session.commit()

	# g = GeneralQuestion.query.all()
	# print(g)

	# of = Offering(2, 2017)
	# db_session.add(of)
	# db_session.commit()
	# oq = Offering.query.all()
	# print(oq)

	# c = Course('comp1531', of)
	# db_session.add(c)
	# db_session.commit()
	# cq = Course.query.all()
	# print(cq)
	

	# GenQs = [] 
	# MCQs = [] 
	# s = Survey('Survey Title', datetime.date(2017, 11, 6), c, GenQs, MCQs)
	# db_session.add(s)
	# db_session.commit()
	# sq = Survey.query.all()
	# print(sq)

	# l = Base.metadata.tables.keys()
	# print(l)



	# user = UniUser.query.get(50)
	# print (user)

	# q_users = db_session.query(UniUser).all()
	# for user in q_users:
	# 	print (user)

	return render_template("home.html")


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

		#no question supplied
		if(question==""):
			general = list(ast.literal_eval(str(GeneralQuestion.query.all())))
			multi = ast.literal_eval(str(MCQuestion.query.all()))
			errorMSG("append.question","No Question Provided")
			return render_template("createquestion.html",multi=multi,general=general)


		#check for invalid characters

		validStrings = copy.copy(answers)
		validStrings.append(question)

		for text in validStrings:
			if (get.cleanString(str(text))==False):
				general = list(ast.literal_eval(str(GeneralQuestion.query.all())))
				multi = ast.literal_eval(str(MCQuestion.query.all()))
				errorMSG("routes.createsurvey","Invalid input in fields")
				return render_template("createquestion.html",multi=multi,general=general)



		#if no answers given then its a generic question
		if(len(answers)==0):
			new = GeneralQuestion(question)
			db_session.add(new)
			db_session.commit()

			general = list(ast.literal_eval(str(GeneralQuestion.query.all())))
			multi = ast.literal_eval(str(MCQuestion.query.all()))

			return render_template("createquestion.html",multi=multi,general=general)


		#if only one answer provided then return with error msg (this is not a valid question)
		if(len(answers)<2):
			questions_pool = fileclasses.question.list()
			return render_template("createquestion.html",multi=multi,general=general)


		#ID = fileclasses.textfile("questionID.txt")
		#qID = ID.updateID()

		#if(qID==""):
		#	questions_pool = fileclasses.question.list()
		#	errorMSG("append.question","No qID Issued")
		#	return render_template("createquestion.html",questions_pool=questions_pool)





		#################old csv method####################

		#update master csv file & survey class

		#answercsv = fileclasses.csvfile("master_question.csv")
		#answercsv.master_question(qID, question, str(answers))

		#Reload in the Question Pool

		#questions_pool = fileclasses.question.list()

		#################new db method######################

		#add question to the general questions only atm just to test



		new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four)
		db_session.add(new)
		db_session.commit()

		#need to make it that we dont bother reading from db again?
		general = list(ast.literal_eval(str(GeneralQuestion.query.all())))
		multi = ast.literal_eval(str(MCQuestion.query.all()))

		return render_template("createquestion.html",multi=multi,general=general)

	else:

		#read in list of questions from db
		general = list(ast.literal_eval(str(GeneralQuestion.query.all())))
		multi = ast.literal_eval(str(MCQuestion.query.all()))

		return render_template("createquestion.html",multi=multi,general=general)


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