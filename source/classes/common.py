from flask import Flask, redirect, render_template, request, url_for
from flask_login import login_user, login_required, current_user, logout_user


#place any classes that are required by multiple files in here!!!!


class Render:
	def home():
		return render_template("home.html", user=current_user)

	def surveys():
		return render_template("surveys.html",user=current_user)

	def modify_survey(surveygen,surveymc,survey,course,general,multi):
		return render_template("modifysurvey.html",user=current_user,
            surveygen=surveygen,surveymc=surveymc,survey=survey,
            course=course,general=general,multi=multi)








class Debug:
	def errorMSG(filename="",msg="",other=""):
		print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+str(msg)+str(other)))