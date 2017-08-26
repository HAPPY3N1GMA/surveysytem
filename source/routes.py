import csv
from flask import Flask, redirect, render_template, request, url_for
from server import app, users

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":

		user = request.form["username"]
		pwd = request.form["password"]

		# Check Password

		if check_password(user,pwd):

			print("Valid password")

			#todo: link to home page

		else:

			print("Incorrect Password")
			
			#make it render saying invalid username/password
			return render_template("index.html", invalid=True)

	return render_template("index.html", invalid=False)


def check_password(user, pwd):

	#if you dont use .get to look inside the dictionary
	#you will get errors if the username is not there
	#.get will return none which is seen as false by the statement

	if pwd == users.get(user):
		return True
	else:
		return False



