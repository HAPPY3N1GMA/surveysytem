import unittest
from flask import Flask
from flask_login import LoginManager
from models import users_model
from authenticate import Credentials, LoginSuccess, LoginFailure

# basic skeletons for unit tests - not functional

# set up testing values (these substitute request.form values)
i = 0; login_inputs = ['1','1'] # add other login values

class LoginTest(unittest.TestCase):

	def test_login_correct_creds(self):
		login = LoginTestable()
		self.assertEqual(login.login_attempt(), redirect(next or url_for('home')))

# had to edit out http requests to be able to make unit tests
class LoginTestable:

	def login_attempt(self):
		credentials = Credentials()
		credentials.username = login_inputs[i]; i=i+1
		credentials.password = login_inputs[i]; i=i+1

		login_status = LoginFailure()

		user = users_model.UniUser.query.get(credentials.get_user())
		if user:
			if credentials.get_pass() == user.password:
				login_status = LoginSuccess()

		return login_status.execute(user)	

test_login = LoginTest()
test_login.test_login_correct_creds()