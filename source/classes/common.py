from flask import Flask, redirect, render_template, request, url_for
from flask_login import login_user, login_required, current_user, logout_user
from models import questions_model



class Render:
    def home():
        return redirect(url_for("home"))

    def surveys():
        return render_template("surveys.html",user=current_user)

    def answer_survey(self,survey,course):
        return render_template("answersurvey.html",survey=survey,course=course)

    def questions():
        general = questions_model.GeneralQuestion.query.all()
        multi = questions_model.MCQuestion.query.all()
        return render_template("questions.html",general=general,multi=multi)

    def modify_question(question):
        return render_template("modifyquestion.html",question=question)

    def modify_survey(surveygen,surveymc,survey,course,general,multi):
        return render_template("modifysurvey.html",user=current_user,
            surveygen=surveygen,surveymc=surveymc,survey=survey,
            course=course,general=general,multi=multi)

    def submit():
        return redirect(url_for("submit"))




class Debug:
    def errorMSG(filename="",msg="",other=""):
        print("\033[91m {}\033[00m" .format("Server Error:"+" ("+filename+") "+str(msg)+str(other)))