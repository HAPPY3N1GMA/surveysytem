import ast, os, time, copy
from classes import authenticate, survey_usage, course_usage, question_usage, common, security
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app
from defines import debug
from functions import get
from models import users_model, surveys_model, questions_model, courses_model
from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user


# create security manager for runtime use
secCheck = security.SecChecks()

@app.route("/")
def index():
	chk = secCheck.authCheck()
	if chk:
		return chk
	return render_template("home.html", user=current_user)

@app.route("/home")
def home():
	chk = secCheck.authCheck()
	if chk:
		return chk
	return render_template("home.html", user=current_user)

@app.route("/submitted")
def submit(): 
	chk = secCheck.authCheck()
	if chk:
		return chk
	return render_template("completed.html")

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
	chk = secCheck.authCheck()
	if chk:
		return chk
	return current_user.registerRequest()


#######################################################################
########################## 	SURVEYS 	###############################
#######################################################################

@app.route("/surveys", methods=["GET", "POST"])
@login_required
def surveys():
	chk = secCheck.authCheck()
	if chk:
		return chk
	if request.method == "GET":
		#this is a temp fix as I dont know how to schedule tasks that work with sqlalchemy
		u_courses = current_user.courses
		for course in u_courses:
			for survey in course.survey:
				survey.status_check()


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
				if request.form['submit'] == '1':
					return survey_usage.StatusSurvey().update_attempt()	
				else:
					return current_user.ViewSurveyResultsRequest(request.form.getlist('surveyid'))
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
	chk = secCheck.authCheck()
	if chk:
		return chk
	if request.method == "GET":
		return current_user.ViewAllQuestions()

	questionform = request.form["questionformid"]
	if questionform=='1':
		return question_usage.OpenQuestion().open_attempt()
	if questionform=='2':
		return question_usage.CreateQuestion().create_attempt()
	if questionform=='3':
		return question_usage.ModifyQuestion().modify_attempt()

	return common.Render.questions()
