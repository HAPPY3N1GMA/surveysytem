import ast, os, time, copy
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app
from defines import debug
from functions import get


from models import users_model, surveys_model, questions_model, courses_model
#from classes import Survey, Course, UniUser, Admin, Staff, Guest, Student


from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user
from util import SurveyUtil, QuestionUtil
from abc import ABCMeta, abstractmethod
from classes import common, course_usage

class Login:

	def login_attempt(self):
		credentials = Credentials()
		credentials.set_user()
		credentials.set_pass()

		login_status = LoginFailure()

		user = users_model.UniUser.query.get(credentials.get_user())
		if user:
			if credentials.get_pass() == user.password:
				login_status = LoginSuccess()

		return login_status.execute(user)		

# abstract
class LoginStatus:
	__metaclass__ = ABCMeta

	@abstractmethod
	def execute(user):
		pass

class LoginSuccess(LoginStatus):
	'purpose: handles case of being a user with correct pass'

	def execute(self, user=None):
		login_user(user)
		next = request.args.get('next')
		if next != None and next != "/logout":
			return redirect(next)
		else:
			return redirect(url_for('home'))

class LoginFailure(LoginStatus):
	'purpose: handles any bad login'

	def execute(self, user=None):
		flash("Invalid Username or Password")
		return render_template("login.html")

class Credentials(object):

	def __init__(self):
		self._username = ''
		self._password = ''

	def set_user(self):
		self._username = request.form["username"]

	def set_pass(self):
		self._password = request.form["password"]

	def get_user(self):
		return self._username

	def get_pass(self):
		return self._password




class Register:

	def register_attempt(self):
		credentials = Credentials()
		credentials.set_user()
		credentials.set_pass()

		password = credentials.get_pass()
		userId = credentials.get_user() 

		register_status = RegisterFailure()
		user = users_model.UniUser.query.get(userId)
		course = course_usage.LoadCourse.load(request.form["regcourse"]) 
		if not user:
			if userId.isdigit():
				if len(password) > 3 and password != 'Password':
					if course:
						register_status = RegisterSuccess()
				else:
					flash("Please Enter a Password of Minimum 4 Characters")	
			else:
				flash("Please Enter a Valid UserId Using Numbers 0-9")
		else:
			flash ('User already registered. Please try another UserId')
		return register_status.execute(userId,password,course)




	def register_approve(self):
		'approve a guest request to answer survey'
		register_status = RegisterApproveFailure()
		
		regId = request.form.getlist("reqid")
		if regId != []:
			registration = users_model.RegistrationRequest.query.get(regId[0])
			if registration:
				course = course_usage.LoadCourse.load(registration.course_id)
				if course:
					register_status = RegisterApproveSuccess()
		else:
			flash("Please Select a Request")

		return register_status.execute(registration)


class RegisterStatus:
	__metaclass__ = ABCMeta

	@abstractmethod
	def execute(self,credentials,course):
		pass

class RegisterSuccess(RegisterStatus):
	'purpose: handles case of being a user with correct pass'

	def execute(self, userId=None, password=None, course=None):
		request = users_model.RegistrationRequest(userId,password,course.id)
		db_session.add(request)
		admin = users_model.UniUser.get_admin()
		admin.reg_requests.append(request)

		db_session.commit()

		flash ('Registration Successful. Please wait for an Admin to approve your request!')
		return redirect("login")

class RegisterFailure(RegisterStatus):
	'purpose: handles any bad registration'

	def execute(self, userId=None, password=None, course=None):
		course_list = courses_model.Course.query.all()
		return render_template("register.html",course_list=course_list)


class RegisterApproveFailure(RegisterStatus):
	'purpose: handles any bad registration'

	def execute(self, userId=None, password=None, course=None):
		return render_template("requests.html")

class RegisterApproveSuccess(RegisterStatus):
	'purpose: adds new user to db, and adds user to course surveys'

	def execute(self, registration):
		user = users_model.Guest(registration.userId,registration.password,'Guest')
		db_session.add(user)

		course = course_usage.LoadCourse.load(registration.course_id)
		user.courses.append(course)

		for survey in course.survey:
			survey.users.append(user)
		
		#remove request
		#request = users_model.RegistrationRequest(userId,password,course.id)

		db_session.delete(registration)
		db_session.commit()

		return render_template("requests.html")