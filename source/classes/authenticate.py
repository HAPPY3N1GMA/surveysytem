import ast, os, time, copy
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, errorMSG
from defines import debug
from functions import get
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
					GeneralResponse, MCResponse
from models import Survey, Course, UniUser, Admin, Staff, Guest, Student
from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user
from util import SurveyUtil, QuestionUtil
from abc import ABCMeta, abstractmethod

class Login:

	def login_attempt(self):
		credentials = Credentials()
		credentials.set_user()
		credentials.set_pass()

		login_status = LoginFailure()
		user = UniUser.query.get(credentials.get_user())

		Role = None
		try:
			Role = eval(UniUser.query.get(credentials.get_user()).role)
		except AttributeError:
			return login_status.execute(user)	

		user = Role.query.get(credentials.get_user())	
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
		return redirect(next or url_for('home'))

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
