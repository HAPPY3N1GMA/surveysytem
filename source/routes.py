import csv, ast, os, time, copy
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, users, authenticated, errorMSG
from defines import debug
from functions import get
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
					GeneralResponse, MCResponse
from models import Survey, Course, UniUser
from database import db_session, Base
from flask_login import login_user, login_required, current_user

#got tired of logging in password each time
if(debug):
	_authenticated = authenticated
else:
	_authenticated = True


@app.route("/")
def index():
	global _authenticated
	#survey_pool = fileclasses.survey.read_all()

	#return render_template("home.html", survey_pool=survey_pool, authenticated=_authenticated)
	return redirect(url_for("admin"))

@app.route("/admin")
def admin(): 
	global _authenticated
	if _authenticated:
		#send the type of user so that we only display what we want them to see!
		admin = False #TEMP hardcoded
		return render_template("admin.html", admin=admin)
	else:
		return redirect(url_for("login"))


@app.route("/submitted")
def submit(): 
	return render_template("completed.html")


#######################################################################
########################## 		LOGIN 	 ##############################
#######################################################################


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
			return redirect(next or url_for('admin'))
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
	# All user attributes can be accessed using the current_user variable
	# which returns None if no logged in user
	print(current_user.is_authenticated)
	print(current_user.password)
	print(current_user.id)

	return redirect(url_for("index"))


@app.route("/home")
def home():
		return redirect(url_for("index"))



#######################################################################
########################## 	SURVEYS 	###############################
#######################################################################



@app.route("/surveys", methods=["GET", "POST"])

def surveys():
	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))

	if request.method == "GET":
		return surveyinfo()
	else:

		#check if an admin and if so, they are permitted to make new surveys!
		admin = False

		surveyform = request.form["surveyformid"]
		if surveyform=='2':
			return opensurvey()		

		if(admin):
			if surveyform=='1':
				return newsurvey()
			if surveyform=='3':
				return removeqsurvey()
			if surveyform=='4':
				return addqsurvey()
			if surveyform=='5':
				return statussurvey()
		else:	
			if surveyform=='6':
				return answersurvey()

		return surveyinfo()


def surveyinfo():
	admin = False
	student = True
	course_list = Course.query.all()
	survey_list = Survey.query.all()
	return render_template("surveys.html",admin=admin,student=student,course_list=course_list,survey_list=survey_list)

def opensurvey():
	admin = False

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

	if not admin:
		print("student opening survey")

		#TODO: check if student answered survey already here!
		if survey.status==1:
			return surveyinfo()

		if survey.status==2:
			return render_template("answersurvey.html",survey=survey,course=course)

	else:
		print("staff opening survey")
		#sort these based on who you are!
		general = GeneralQuestion.query.all()
		multi = MCQuestion.query.all()

		surveygen = survey.gen_questions
		surveymc = survey.mc_questions

		return render_template("modifysurvey.html",admin=admin,surveygen=surveygen,surveymc=surveymc,survey=survey,course=course,general=general,multi=multi)


def newsurvey():
	admin = False

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

def statussurvey():
	print("changing survey status")

	#check if they have authority to do this!

	surveyID = request.form["surveyid"]

	survey = Survey.query.filter_by(id=surveyID).first()	
	if(survey==None):
		errorMSG("routes.opensurvey","survey object is empty")
		return surveyinfo()	

	if survey.status == 0:
		survey.status = 1
	elif survey.status == 1:
		survey.status = 2
	else:
		return viewsurvey()
	db_session.commit()

	return opensurvey()

def viewsurvey():
	print("view survey results now")

	#temp
	return opensurvey()


def answersurvey():
	print("answering survey")

	#check student answered all fields
	surveyID = request.form["surveyid"]

	survey = Survey.query.filter_by(id=surveyID).first()	
	if(survey==None):
		errorMSG("routes.answersurvey","survey object is empty")
		return surveyinfo()	

	course = Course.query.filter_by(id=survey.course_id).first()	
	if(course==None):
		errorMSG("routes.answersurvey","course object is empty")
		return surveyinfo()

	print("length:",len(survey.gen_questions))

	genResponseList = []
	if len(survey.gen_questions)>0:

		genResponseList = request.form.getlist('genResponse')
		genResponseList = list(filter(None, genResponseList))

		if len(survey.gen_questions)!=len(genResponseList):
			errorMSG("routes.answersurvey","Extended Response Questions not completed")
			return opensurvey()

	for text in genResponseList:
		if (get.cleanString(str(text))==False):
			errorMSG("routes.answersurvey","Invalid input in extended response")
			return opensurvey()


	mcResponseList = []
	if len(survey.mc_questions)>0:
		for question in survey.mc_questions:
			if (request.form.getlist(str(question.id))==[]):
				errorMSG("routes.answersurvey","MultiChoice Questions not completed")
				return opensurvey()
			mcResponseList.append(request.form[str(question.id)])

	mcResponseList = list(filter(None, mcResponseList))

	if len(survey.mc_questions)!=len(mcResponseList):
		errorMSG("routes.answersurvey","MultiChoice Questions not completed")
		return opensurvey()

	print("mcResponseList:",mcResponseList)


		#TODOcheck that the responses have valid characters



	#see if there is already a survey response 

	surveyResponse = SurveyResponse(survey.id)
	db_session.add(surveyResponse)


	#QuestionResponse(surveyResponse.id, mcquestionid, genquestionid,
    #             answer)


	#surveyResponse.id

	#this sorts and stores the questions into the survey
	for question,response in zip(survey.gen_questions,genResponseList):
		print(response)


	for question,response in zip(survey.mc_questions,mcResponseList):
		print(response)
		response = MCResponse(surveyResponse.id,question.id,response)
		surveyResponse.mc_responses.append(response)


	db_session.commit()



	#save all fields


	#set survey to completed by this student to prevent resubmission









	#temp
	return surveyinfo()






#######################################################################
########################## 	 DB TEST 	###############################
#######################################################################

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


#######################################################################
########################## 	 QUESTIONS 	###############################
#######################################################################

@app.route('/questions', methods=["GET", "POST"])
def questions():
	global _authenticated
	if not _authenticated:
		return redirect(url_for("login"))

	if request.method == "GET":
		return questioninfo()
	else:

		#check if an admin and if so, they are permitted to make new questions!
		admin = False

		if(admin):
			questionform = request.form["questionformid"]
			if questionform=='1':
				return openquestion()
			if questionform=='2':
				return addquestion()
			if questionform=='3':
				return removequestion()
			if questionform=='4':
				return modifyquestion()

		return questioninfo()

def questioninfo():
	print("questioninfo")
	admin = False

	#read in list of questions from db, filter out any not available to user or deleted
	general = GeneralQuestion.query.all()
	multi = MCQuestion.query.all()
	return render_template("questions.html",admin=admin,multi=multi,general=general)


def openquestion():
	print("open question")

	if (request.form.getlist('question')==[]):
		errorMSG("routes.openquestion","question not selected")
		return questioninfo()		

	qID = request.form['question']
	questionType = 1

	#load up the question from db
	if (qID[1:2]=='0'):	
		questionObject = MCQuestion.query.filter_by(id=int(qID[4:5])).first()
	elif (qID[1:2]=='1'):
		questionObject = GeneralQuestion.query.filter_by(id=int(qID[4:5])).first()
		questionType = 2 #so we know if question type was modified in form
	if (questionObject==None):
		errorMSG("routes.openquestion","This question does not exist")
		return questioninfo()

	return render_template("modifyquestion.html",questionObject=questionObject,questionType=questionType)


def addquestion():

	#check user is admin
	admin = False

	if not admin:
		errorMSG("routes.addquestion","Unknown user attempted to add question")
		return questioninfo()

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
		return questioninfo()

	for text in question:
		if (get.cleanString(str(text))==False):
			errorMSG("routes.createsurvey","Invalid input in fields")
			return questioninfo()


	if(request.form["qtype"]=='0'):
		new = GeneralQuestion(question,status)
		db_session.add(new)
		db_session.commit()
		return questioninfo()

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
			return questioninfo()


	#if only one answer provided then return with error msg (this is not a valid question)
	if(len(answers)<2):
		errorMSG("routes.createsurvey","Only one answer provided for a mc question")
		return questioninfo()

	new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
	db_session.add(new)
	db_session.commit()

	return questioninfo()


def modifyquestion():

	print("modify question")

	oldType = request.form["oldType"]
	qID = request.form["qID"]
	question = request.form["questiontitle"]


	print("oldType:",oldType, "qID:",qID )

	status = 0

	if(request.form.getlist("optional")!=[]):
		status = 1

	if(request.form["delete"]=='1'):
		#im deleting this question
		status = 2
	else:
		if(question==""):
			errorMSG("append.question","No Question Provided")
			return questioninfo()

		for text in question:
			if (get.cleanString(str(text))==False):
				errorMSG("routes.modifyquestion","Invalid input in fields")
				return openquestion()

	#old question object being modified
	if(oldType=='2'):
		print("im a general question modificiation")
		qObject=GeneralQuestion.query.filter_by(id=qID).first()
	else:
		print("im a mc question modificiation")
		qObject=MCQuestion.query.filter_by(id=qID).first()	


	if(qObject==None):
		errorMSG("routes.modifyquestion ","No question object Found")
		return questioninfo()

	#is the question just getting deleted?
	if(status==2):
		print("Question ID:",qObject.id,"Title: ",qObject.question, "im getting deleted now")
		qObject.status = status
		db_session.commit()
		return questioninfo()


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
		return questioninfo()	


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
			return openquestion()


	#if only one answer provided then return with error msg (this is not a valid question)
	if(len(answers)<2):
		errorMSG("routes.createsurvey","Only one answer provided for a mc question")
		return openquestion()

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
	return questioninfo()
























































