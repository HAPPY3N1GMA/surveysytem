import ast, os, time, copy
from classes import authenticate
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, errorMSG
from defines import debug
from functions import get
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
					GeneralResponse, MCResponse
from models import Survey, Course, UniUser
from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user
from util import SurveyUtil, QuestionUtil

@app.route("/")
def index():
	if (current_user.is_authenticated):
		return render_template("home.html", user=current_user)
	else:
		return redirect(url_for("login"))

@app.route("/home")
def home():
	if (current_user.is_authenticated):
		return render_template("home.html", user=current_user)
	else:
		return redirect(url_for("login"))


@app.route("/submitted")
def submit(): 
	if (current_user.is_authenticated):
		return render_template("completed.html")

#######################################################################
##########################     Results   ##############################
#######################################################################

@app.route("/results/<id>")
@login_required
def results(id):
	survey = Survey.query.get(id)
	responses = survey.responses

	mc_responses = []
	for response in responses:
		for mc_response in response.mc_responses:
			mc_responses.append(mc_response)

	list_of_lists = []
	# for each question in survey
	for question in survey.mc_questions:
		question_res = []
	# iterate through responses 
		for response in mc_responses:
			# find responses with same questionid
			if question.id == response.question_id:
				# add them to the question specific
				question_res.append(response)
		list_of_lists.append(question_res)

	print(list_of_lists)

	return render_template("results.html", list_of_lists=list_of_lists)




#######################################################################
########################## 		LOGIN 	 ##############################
#######################################################################


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		attempt = authenticate.Login()
		return attempt.login_attempt()

	return render_template("login.html")


@app.route("/logintest")
@login_required
def test():
	# All user attributes can be accessed using the current_user variable
	# which returns None if no logged in user
	print(current_user.is_authenticated)
	print(current_user.password)
	print(current_user.id)
	print(current_user.courses)

	return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect("login")


#######################################################################
######################## 		REGISTER 	    #######################
#######################################################################

@app.route("/register", methods=["GET", "POST"])
def register():
	if (current_user.is_authenticated):
		return redirect(url_for("home"))

	if request.method == 'POST':
		util = SurveyUtil()
		return util.registeruser()

	course_list = Course.query.all()
	return render_template("register.html",course_list=course_list)


#######################################################################
########################## 	SURVEYS 	###############################
#######################################################################

@app.route("/surveys", methods=["GET", "POST"])
@login_required
def surveys():
	util = SurveyUtil()
	if (current_user.is_authenticated)==False:
		return redirect(url_for("login"))

	if request.method == "GET":
		return util.surveyinfo()
	else:

		#check if an admin and if so, they are permitted to make new surveys!
		surveyform = request.form["surveyformid"]
		if surveyform=='2':
			return util.opensurvey()		

		if(current_user.role == 'admin' or current_user.role == 'staff'):
			if(current_user.role=='admin'):
				if surveyform=='1':
					return util.newsurvey()
				if surveyform=='3':
					return util.removeqsurvey()
				if surveyform=='4':
					return util.addqsurvey()
				if surveyform=='5':
					return util.statussurvey()

			if request.form.getlist("surveyid")==[]:
				errorMSG("routes.surveys","survey doesnt exist")
				return util.surveyinfo()	

			surveyID = request.form["surveyid"]
			survey = Survey.query.filter_by(id=surveyID).first()	
			if(survey==None):
				errorMSG("routes.surveys","survey object is empty")
				return util.surveyinfo()	


			#enrolled staff have access to modify surveys
			if current_user in survey.users and survey.status==1:
				if surveyform=='3':
					return util.removeqsurvey()
				if surveyform=='4':
					return util.addqsurvey()
				if surveyform=='5':
					return util.statussurvey()
		else:
		#students can only answer the survey
			if surveyform=='6':
				return util.answersurvey()

		return util.surveyinfo()


#######################################################################
########################## 	 QUESTIONS 	###############################
#######################################################################

@app.route('/questions', methods=["GET", "POST"])
@login_required
def questions():
	util = QuestionUtil()
	if (current_user.is_authenticated)==False:
		return redirect(url_for("login"))

	if(current_user.role != 'admin'):
		errorMSG("routes.questions","unauthorised user attempted access:",current_user.id)
		return render_template("home.html", user=current_user)

	if request.method == "GET":
		return util.questioninfo()

	questionform = request.form["questionformid"]
	if questionform=='1':
		return util.openquestion()
	if questionform=='2':
		return util.addquestion()
	if questionform=='3':
		return util.removequestion()
	if questionform=='4':
		return util.modifyquestion()

	return util.questioninfo()


























































