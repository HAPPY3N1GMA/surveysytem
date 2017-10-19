import ast, os, time, copy
from classes import authenticate, survey_usage, course_usage
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app
from defines import debug
from functions import get
#from models import GeneralQuestion, MCQuestion, SurveyResponse,\
#					GeneralResponse, MCResponse
from models import users_model, surveys_model, questions_model, courses_model
from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user
from util import SurveyUtil, QuestionUtil
from classes import common

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

	# all this can be redirected and run by:
	# return current_user.ViewSurveyResults()
	# or via survey_usage..... something or other to make it abstracted and constant with others


	#also note: view results currently work sfor staff at any point as its a link always enabled!!!! 
	#button should be disabled in the html


	survey = surveys_model.Survey.query.get(id)
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

	course_list = courses_model.Course.query.all()
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
		surveyform = request.form.getlist("surveyformid")
		if surveyform == []:
			return redirect(url_for("home"))

		surveyform = surveyform[0]
			
		if surveyform=='1':
			return survey_usage.CreateSurvey().create_attempt()	
		if surveyform=='2':
			return survey_usage.OpenSurvey().open_attempt()		

		if surveyform=='5':
			return survey_usage.StatusSurvey().update_attempt()	


		if(current_user.role == 'Admin' or current_user.role == 'Staff'):
			if(current_user.role=='Admin'):
				# if surveyform=='1':
				# 	return util.newsurvey()
				if surveyform=='3':
					return util.removeqsurvey()
				if surveyform=='4':
					return util.addqsurvey()
				

			if request.form.getlist("surveyid")==[]:
				common.Debug.errorMSG("routes.surveys","survey doesnt exist")
				return util.surveyinfo()	

			surveyID = request.form["surveyid"]
			survey = surveys_model.Survey.query.filter_by(id=surveyID).first()	
			if(survey==None):
				common.Debug.errorMSG("routes.surveys","survey object is empty")
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

	if(current_user.role != 'Admin'):
		common.Debug.errorMSG("routes.questions","unauthorised user attempted access:",current_user.id)
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


























































