import csv, ast, os, time, copy
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, users, authenticated, errorMSG
from functions import append, get
from classes import fileclasses
from defines import masterSurveys, masterQuestions, debug
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
					QuestionResponse
from models import Survey, Course, UniUser
from database import db_session, Base
from flask_login import login_user, login_required

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
		return render_template("admin.html")
	else:
		return redirect(url_for("login"))


@app.route("/submitted")
def submit(): 
	return render_template("completed.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		id = request.form['username']
		password = request.form['password']
		user = UniUser.query.get(id)
		if password == user.password:
			login_user(user)
			flash('Logged in successfully.')
			next = request.args.get('next')
			return redirect(next or url_for('index'))
		else:
			return render_template("login.html", invalid=True)

	return render_template("login.html", invalid=False)


def check_password(user, pwd):
	if pwd == users.get(user):
		return True
	else:
		return False


@app.route("/logintest")
@login_required
def test():
		return redirect(url_for("login"))


@app.route("/home")
def home():
		return redirect(url_for("index"))


@app.route("/surveys", methods=["GET", "POST"])

def surveys():
	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))

	if request.method == "GET":
		return surveyinfo()
	else:

		#check if an admin and if so, they are permitted to make new surveys!
		admin = True
		student = False

		if(student==False):
			surveyform = request.form["surveyformid"]
			if surveyform=='1':
				return newsurvey()
			if surveyform=='2':
				return opensurvey()
			if surveyform=='3':
				return removeqsurvey()
			if surveyform=='4':
				return addqsurvey()

		return surveyinfo()


def surveyinfo():
	admin = True
	student = False
	course_list = Course.query.all()
	survey_list = Survey.query.all()
	return render_template("surveys.html",admin=True,course_list=course_list,survey_list=survey_list)

def opensurvey():
	admin = True
	student = False

	if (request.form.getlist("surveyid")==[]):
		errorMSG("routes.opensurvey","surveyid not selected")
		return surveyinfo()
	
	surveyID = request.form["surveyid"]

	survey = Survey.query.filter_by(id=surveyID).first()	
	if(survey==None):
		errorMSG("routes.opensurvey","survey object is empty")
		return surveyinfo()	

	course = Course.query.filter_by(id=survey.course_id).first()	
	if(course==None):
		errorMSG("routes.opensurvey","course object is empty")
		return surveyinfo()

	if student:
		print("student opening survey")
		return surveyinfo()
		return render_template("viewsurvey.html",admin=admin,survey=survey,course=course)

	else:
		print("staff opening survey")
		#sort these based on who you are!
		general = GeneralQuestion.query.all()
		multi = MCQuestion.query.all()

		surveygen = survey.gen_questions
		surveymc = survey.mc_questions

		return render_template("modifysurvey.html",admin=admin,surveygen=surveygen,surveymc=surveymc,survey=survey,course=course,general=general,multi=multi)


def newsurvey():
	admin = True
	student = False

	survey_name = request.form["svyname"]
	courseID = request.form["svycourse"]

	#qObject=Course.query.filter_by(id=courseID).first()

	if (get.cleanString(str(survey_name))==False):
		errorMSG("routes.newsurvey","Invalid Characters in survey name")
		return surveyinfo()

	if (str(courseID) == ''):
		errorMSG("routes.newsurvey","No course selected")
		return surveyinfo()

	#new survey created then redirect to the modify survey page to add questions etc
	survey = Survey(survey_name,datetime.now(),courseID)
	db_session.add(survey)
	db_session.commit()

	return surveyinfo()


def addqsurvey():
	print("add question to survey")

	#check they are staff first


	#get list of questions to add
	survey_questions = request.form.getlist('question')

	if survey_questions==[]:
		errorMSG("routes.addqsurvey","no questions selected")
		return opensurvey()


	if (request.form.getlist("surveyid")==[]):
		errorMSG("routes.opensurvey","surveyid not selected")
		return surveyinfo()
	
	surveyID = request.form["surveyid"]

	survey = Survey.query.filter_by(id=surveyID).first()	
	if(survey==None):
		errorMSG("routes.opensurvey","survey object is empty")
		return surveyinfo()	

	#this sorts and stores the questions into the survey
	for question in survey_questions:
		if (question[1:2]=='0'):	
			question = MCQuestion.query.filter_by(id=int(question[4:5])).first()
			survey.mc_questions.append(question)
		elif (question[1:2]=='1'):
			question = GeneralQuestion.query.filter_by(id=int(question[4:5])).first()
			survey.gen_questions.append(question)

	db_session.commit()

	#reload page
	return opensurvey()

def removeqsurvey():
	#get question to remove
	print("remove question from survey")

	
	if request.form.getlist('question')==[]:
		errorMSG("routes.addqsurvey","no questions selected")
		return opensurvey()

	survey_question = request.form['question']

	if (request.form.getlist("surveyid")==[]):
		errorMSG("routes.opensurvey","surveyid not selected")
		return surveyinfo()
	
	surveyID = request.form["surveyid"]
	survey = Survey.query.filter_by(id=surveyID).first()	
	if(survey==None):
		errorMSG("routes.opensurvey","survey object is empty")
		return surveyinfo()	

	#remove question from the survey
	if (survey_question[1:2]=='0'):	
		question = MCQuestion.query.filter_by(id=int(survey_question[4:5])).first()
		survey.mc_questions.remove(question)
	elif (survey_question[1:2]=='1'):
		question = GeneralQuestion.query.filter_by(id=int(survey_question[4:5])).first()
		survey.gen_questions.remove(question)

	db_session.commit()



	return opensurvey()





#old method
@app.route("/createsurvey", methods=["GET", "POST"])
def createsurvey():

	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))



	#only admins can access this page

	if request.method == "POST":

		#we need to know what kind of user you are, staff, admin


		survey_name = request.form["svyname"]
		survey_name = str(survey_name)
		survey_course = request.form["svycourse"]
		survey_date = time.strftime("%d/%m/%Y,%I:%M:%S")
		survey_questions = request.form.getlist('question')


		general_question = []
		multi_question = []

		#this sorst out the returned list of questions into 2 lists of qid's
		for question in survey_questions:
			if (question[1:2]=='0'):
				multi_question.append(int(question[4:5]))
			elif (question[1:2]=='1'):
				general_question.append(int(question[4:5]))

		#we now have the index numbers of the questions we want added to the survey



		print("general_question: ",general_question)

		print("multi_question: ",multi_question)

		if(True == False):

			if (get.cleanString(str(survey_name))):
				if (survey_name == "" or survey_course == "" or survey_date == "" or survey_questions == []):
					errorMSG("routes.createsurvey","Invalid input in fields")
				else:


					survey_questions = list(survey_questions)

					general_question = []
					multi_question = []

					for question in survey_questions:
						if (question[0]=='general'):
							general_question.append(question[1])
						elif (question[0]=='multi'):
							multi_question.append(question[1])



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


	#we need to know what kind of user you are, staff, admin

	#to determine what kind of questions you even get served

	#Populate Question and Course lists
	#questions_pool = fileclasses.question.list()
	course_list = fileclasses.course.readall()


	general = list(ast.literal_eval(str(GeneralQuestion.query.all())))
	multi = ast.literal_eval(str(MCQuestion.query.all()))
	return render_template("createsurvey.html",multi=multi,general=general,course_list = course_list)


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


@app.route('/modifyquestion/<int:Questiontype>/<int:qID>', methods=["GET", "POST"])
def modifyquestion(Questiontype=-1, qID=-1):

	if not _authenticated:
		return redirect(url_for("login"))


	#if not admin then exit as well!


	if request.method == "GET":
		#check params set
		if(Questiontype==-1 or qID==-1):
			return redirect(url_for("createquestion"))

		#get the qid info from the db
		questionInfo = []
		if(Questiontype==1):
			#mc type question
			questionInfo = db_session.query(MCQuestion).get(qID)

		else:

			questionInfo = db_session.query(GeneralQuestion).get(qID)

		if(questionInfo==[]):
			#error modifying question it oculdnt 
			errorMSG("routes.modifyquestion","Unable to locate question in db -- ","Qtype:",qType,"qID",qID)
			return redirect(url_for("createquestion"))

		#return render_template("modifyquestion.html")
		return render_template("modifyquestion.html",Questiontype=Questiontype,questionInfo=questionInfo)

	else:

		oldType = request.form["oldType"]
		qID = request.form["qID"]
		question = request.form["question"]

		status = 0

		if(request.form.getlist("optional")!=[]):
			status = 1

		if(request.form["delete"]=='1'):
			status = 2

		if(question==""):
			errorMSG("append.question","No Question Provided")
			return redirect(url_for("createquestion"))

		for text in question:
			if (get.cleanString(str(text))==False):
				errorMSG("routes.modifyquestion","Invalid input in fields")
				return redirect(url_for("createquestion"))

		#old question object being modified
		if(oldType=='2'):
			qObject=GeneralQuestion.query.filter_by(id=qID).first()
		else:
			qObject=MCQuestion.query.filter_by(id=qID).first()	


		if(qObject==None):
			errorMSG("routes.modifyquestion ","No question object Found")
			return redirect(url_for("createquestion"))

		#is the question getting deleted?
		if(status==2):
			qObject.status = status
			db_session.commit()
			return redirect(url_for("createquestion"))


		#extended response questions
		if(request.form["qtype"]=='0'):
			if(oldType=='2'):
				#same general type of question, just changing fields
				qObject.question = question
				qObject.status = status

			else:
				#change of question type - delete old type, and make new type
				qObject.status = 2
				new = GeneralQuestion(question,status)
				db_session.add(new)
				
			db_session.commit()	
			return redirect(url_for("createquestion"))	


		#multiple choice question
		answer_one = request.form["option_one"]
		answer_two = request.form["option_two"]
		answer_three = request.form["option_three"]
		answer_four = request.form["option_four"]

		#check for invalid characters
		answers = [answer_one,answer_two,answer_three,answer_four]
		answers = list(filter(None, answers))
		validStrings = copy.copy(answers)
		validStrings.append(question)


		for text in validStrings:
			if (get.cleanString(str(text))==False):
				errorMSG("routes.createsurvey","Invalid input in fields")
				return redirect(url_for("createquestion"))


		#if only one answer provided then return with error msg (this is not a valid question)
		if(len(answers)<2):
			errorMSG("routes.createsurvey","Only one answer provided for a mc question")
			return redirect(url_for("createquestion"))

		if(oldType=='1'):
			#same mc question, just update all the fields
			qObject.question = question
			qObject.status = status
			qObject.answerOne = answer_one
			qObject.answerTwo = answer_two
			qObject.answerThree = answer_three
			qObject.answerFour = answer_four	
		else:
			#new mc question, set old question to deleted, and make new question
			qObject.status = 2
			new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
			db_session.add(new)
		
		db_session.commit()
		return redirect(url_for("createquestion"))



@app.route("/createquestion", methods=["GET", "POST"])
def createquestion():
	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))

	if request.method == "POST":
		if request.form.getlist("formID")==['1']:
			#redirect to create question
			return createquestionresponse()
		elif (request.form.getlist("multiEdit")!=[]):
			#multiple choice type question
			return redirect(url_for("modifyquestion", Questiontype=1, qID=request.form["multiEdit"]))
		elif (request.form.getlist("generalEdit")!=[]):
			#general question type
			return redirect(url_for("modifyquestion", Questiontype=2, qID=request.form["generalEdit"]))
	
	return createquestionload()

def createquestionresponse():

	#TODO: Display Error to user adding question if they forget fields

	question = request.form["question"]
	status = 0

	#by default a question is mandatory unless optional is checked
	if(request.form.getlist("optional")!=[]):
		status = 1


	#todo:
	#create class to add general question, and mc questions
	#class to clean a string passed to it and return 1/0 clean or unclean
	#make this function use these new classes
	#we need to add to db, that a question is set as optional/mandatory
	#as per the specsheet


	if(question==""):
		errorMSG("append.question","No Question Provided")
		return createquestionload()

	for text in question:
		if (get.cleanString(str(text))==False):
			errorMSG("routes.createsurvey","Invalid input in fields")
			return createquestionload()


	if(request.form["qtype"]=='0'):
		new = GeneralQuestion(question,status)
		db_session.add(new)
		db_session.commit()
		return createquestionload()

	#multiple choice question
	answer_one = request.form["option_one"]
	answer_two = request.form["option_two"]
	answer_three = request.form["option_three"]
	answer_four = request.form["option_four"]

	#check for invalid characters
	answers = [answer_one,answer_two,answer_three,answer_four]
	answers = list(filter(None, answers))
	validStrings = copy.copy(answers)
	validStrings.append(question)

	for text in validStrings:
		if (get.cleanString(str(text))==False):
			errorMSG("routes.createsurvey","Invalid input in fields")
			return createquestionload()


	#if only one answer provided then return with error msg (this is not a valid question)
	if(len(answers)<2):
		errorMSG("routes.createsurvey","Only one answer provided for a mc question")
		return createquestionload()

	new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
	db_session.add(new)
	db_session.commit()
	return createquestionload()

def createquestionload():
	#read in list of questions from db, ignoring any that are deleted
	multi = [row for row in list(ast.literal_eval(str(MCQuestion.query.all()))) if row[3]!=2]
	general = [row for row in list(ast.literal_eval(str(GeneralQuestion.query.all()))) if row[2]!=2]


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