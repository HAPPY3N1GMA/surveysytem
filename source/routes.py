import csv
from flask import Flask, redirect, render_template, request, url_for
from server import app, users

authenticated = 0

@app.route("/", methods=["GET", "POST"])
def index():
	global authenticated
	authenticated = 0
	if request.method == "POST":

		user = request.form["username"]
		pwd = request.form["password"]

		# Check Password

		if check_password(user,pwd):
			
			print("Valid password")
			authenticated = 1
			return redirect(url_for("home"))

		else:

			print("Invalid Password") #tmp

			return render_template("index.html", invalid=True)


def check_password(user, pwd):

	#if you dont use .get to look inside the dictionary
	#you will get errors if the username is not there
	#.get will return none which is seen as false by the statement

	if pwd == users.get(user):
		return True
	else:
		return False

@app.route("/home")
def home():
	# button to go to questions
	# button to go to surveys
	global authenticated
	if (authenticated):
		return render_template("home.html")
	else:
		return redirect(url_for("index"))