import ast, os, time, copy
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, errorMSG
from defines import debug
from functions import get
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
                    GeneralResponse, MCResponse
from models import Survey, Course, UniUser
from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user
from util import SurveyUtil, QuestionUtil
from abc import ABCMeta, abstractmethod
from classes import course

# needs to;
# Handles who does what with a survey
# 1. load up a particular survey
# 2. load up the course that relates to the survey
# 3. user dependent (abstract)
#   student : depending on survey status either pass or taken to answer page or to results
#   anyone else in course who isnt student : taken to modify page 

class ListSurveys:
    def show_list(self):
        return render_template("surveys.html",user=current_user)

class OpenSurvey:
    
    def open_attempt(self):
        survey = LoadSurvey.load()
        if survey:
            course = course.LoadCourse.load(survey.course_id)
            if course:
                if survey.status == 1:
                    return current_user.ModifySurvey(survey, course)
                if survey.status == 2:
                    return current_user.AnswerSurvey(survey, course)
                if survey.status == 3:
                    return current_user.ViewSurveyResults(survey, course)
        return  ListSurveys.show_list()

class LoadSurvey:
    'loads a specific survey'

    def load():
        if err_check():
            surveyID = request.form["surveyid"]
            survey = Survey.query.filter_by(id=surveyID).first()    
            return survey
        return None

    def err_check():
        if (request.form.getlist("surveyid") == []):
            errorMSG("routes.opensurvey", "surveyid not selected")
            return False
        return True
        