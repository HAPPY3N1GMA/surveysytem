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
from classes import common, security

# create security manager for runtime use
secCheck = security.SecChecks()

@app.route("/")
def index():

	secCheck.authCheck()
	return render_template("home.html", user=current_user)

@app.route("/home")
def home():

	secCheck.authCheck()
	return render_template("home.html", user=current_user)

@app.route("/submitted")
def submit(): 

	secCheck.authCheck()
	return render_template("completed.html")

#######################################################################
##########################     Results   ##############################
#######################################################################

@app.route("/results/<id>/<qid>")
@login_required
def results(id, qid):

# all this can be redirected and run by:
	# return current_user.ViewSurveyResults()
	# or via survey_usage..... something or other to make it abstracted and constant with others


	#also note: view results currently work sfor staff at any point as its a link always enabled!!!! 
	#button should be disabled in the html


	survey = surveys_model.Survey.query.get(id)
	question = questions_model.MCQuestion.query.get(qid)
	responses = survey.responses
	num_responses = len(responses)
	print(num_responses)

	mc_responses = []
	for response in responses:
			for mc_response in response.mc_responses:
				if str(mc_response.question_id) == qid:
					mc_responses.append(mc_response)

	list_of_lists = []
	print(mc_responses)
	# for each question in survey
	# for question in survey.mc_questions:
	# 	question_res = []
	# # iterate through responses 
	# 	for response in mc_responses:
	# 		# find responses with same questionid
	# 		if question.id == response.question_id:
	# 			# add them to the question specific
	# 			question_res.append(response)
	# 	list_of_lists.append(question_res)

	# print(list_of_lists)

	colours = []
	labels = []
	data = []  # the above list in percentages
	# for each group of question responses
	a_one = 0
	a_two = 0
	a_th = 0
	a_four = 0
	for resp in mc_responses:
		print("Question id" + str(resp.question_id))
		print("   Response: " + resp.response)
		if resp.response == '1':
			a_one += 1
		if resp.response == '2':
			a_two += 1
		if resp.response == '3':
			a_th += 1
		if resp.response == '4':
			a_four += 1
	data.append(a_one/num_responses)
	data.append(a_two/num_responses)
	data.append(a_th/num_responses)
	data.append(a_four/num_responses)
	labels.append(question.answerOne)
	labels.append(question.answerTwo)
	labels.append(question.answerThree)
	labels.append(question.answerFour)
	colours.append("red")
	colours.append("green")
	colours.append("blue")
	colours.append("yellow")
	
	print(data)

	return render_template("results.html", qid=qid,
										   data=data,
										   labels=labels,
										   survey=survey,
										   responses=responses,
										   question=question)

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
		attempt = authenticate.Register()
		return attempt.register_attempt()

	course_list = courses_model.Course.query.all()
	return render_template("register.html",course_list=course_list)



#######################################################################
######################## 		REGISTER 	    #######################
#######################################################################

@app.route("/requests", methods=["GET", "POST"])
def requests():
	if (current_user.is_authenticated):
		if(current_user.role == 'Admin'):
			if request.method == 'POST':
				attempt = authenticate.Register()
				return attempt.register_approve()
			else:
				return render_template("requests.html")

	return redirect(url_for("home"))

#######################################################################
########################## 	SURVEYS 	###############################
#######################################################################

@app.route("/surveys", methods=["GET", "POST"])
@login_required
def surveys():

	secCheck.authCheck()
	util = SurveyUtil()

	if request.method == "GET":
		return common.Render.surveys()
	else:
		surveyform = request.form.getlist("surveyformid")
		if surveyform:
			surveyform = surveyform[0]
			if surveyform=='1':
				return survey_usage.CreateSurvey().create_attempt()	
			if surveyform=='2':
				return survey_usage.OpenSurvey().open_attempt()	
			if surveyform=='3':
				return survey_usage.RemoveQuestionSurvey().remove_attempt()
			if surveyform=='4':
				return survey_usage.AddQuestionSurvey().add_attempt()
			if surveyform=='5':
				return survey_usage.StatusSurvey().update_attempt()	
			if surveyform=='6':
				return survey_usage.AnswerSurvey().answer_attempt()	

			return common.Render.surveys()

	return redirect(url_for("home"))

#######################################################################
########################## 	 QUESTIONS 	###############################
#######################################################################

@app.route('/questions', methods=["GET", "POST"])
@login_required
def questions():

	secCheck.authCheck()
	util = QuestionUtil()

	if request.method == "GET":
		return current_user.ViewAllQuestions()

	questionform = request.form["questionformid"]
	if questionform=='1':
		# return question_usage.OpenQuestion()
		return util.openquestion()
	if questionform=='2':
		# return question_usage.AddQuestion()
		return util.addquestion()
	if questionform=='3':
		# return question_usage.RemoveQuestion()
		return util.removequestion()
	if questionform=='4':
		# return question_usage.ModifyQuestion()
		return util.modifyquestion()

	return util.questioninfo()
