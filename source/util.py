import copy
from datetime import datetime
from flask import redirect, render_template, request, url_for, flash
from functions import get
# from models import questions_model.GeneralQuestion, questions_model.MCQuestion, surveys_model.SurveyResponse,\
# 					questions_model.GeneralResponse, questions_model.MCResponse
#from models import surveys_model.Survey, courses_model.Course, users_model.UniUser

from models import users_model, surveys_model, questions_model, courses_model

from database import db_session
from flask_login import current_user
from classes import survey_usage, common, course_usage, security

# create security manager for runtime use
secCheck = security.SecChecks()

class SurveyUtil(object):
    'provides all utilities for surveys'

    def surveyinfo(self):
        return render_template("surveys.html",user=current_user)

    def viewsurvey(self):
        secCheck.authCheck()
        print("attempting to view survey")
        return survey_usage.OpenSurvey().open_attempt()	

##############################################################        

class QuestionUtil(object):
    'provides all utilities for questions'

