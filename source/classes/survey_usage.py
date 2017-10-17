import ast, os, time, copy
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, errorMSG
from defines import debug
from functions import get
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
                    GeneralResponse, MCResponse
from models import Survey, Course, UniUser, Admin, Staff, Student, Guest
from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user
from abc import ABCMeta, abstractmethod
from classes import course_usage


class ListSurveys:
    def show_list():
        return render_template("surveys.html",user=current_user)


class CreateSurvey:
    'creates a new survey'
    def create_attempt(self):
        courseId = request.form["svycourse"]
        surveyName = request.form["svyname"]
        startDate = request.form["startdate"]
        endDate = request.form["enddate"]

        if CreateSurvey.err_check(courseId,surveyName,startDate,endDate):
            startDate = datetime.strptime(startDate, '%Y/%m/%d')
            endDate = datetime.strptime(endDate, '%Y/%m/%d')
            return current_user.CreateSurvey(courseId,surveyName,startDate,endDate)

        return ListSurveys.show_list()


    def err_check(courseId='',surveyName='',startDate='',endDate=''):
        'checks a new surveys form fields'
        if surveyName == '':
            flash('Please Enter a Valid Survey Name')
            return False

        if (get.cleanString(str(surveyName)) == False):
            errorMSG("routes.newsurvey", "Invalid Characters in survey name")
            return False

        if (courseId == ''):
            errorMSG("routes.newsurvey", "No course ID selected")
            return False

        try:
            startDate = datetime.strptime(startDate, '%Y/%m/%d')
            endDate = datetime.strptime(endDate, '%Y/%m/%d')
        except ValueError:
            flash('Please Enter a Start and Finish Date')
            return False
        
        course = Course.query.filter_by(id=courseId).first()    
        if(course == None):
            errorMSG("routes.newsurvey", "course object is empty")
            return False

        if(Survey.query.filter_by(course_id=courseId).first() != None):
            errorMSG("routes.newsurvey", "survey already exists!")
            return False

        return True


class OpenSurvey:
    'opens a specific survey to required page'
    def open_attempt(self):
        survey = LoadSurvey.load(request.form["surveyid"])
        if survey:
            course = course_usage.LoadCourse.load(survey.course_id)  
            if course:
                if survey.status < 2:
                    return current_user.ModifySurvey(survey, course)
                if survey.status == 2:
                    return current_user.AnswerSurvey(survey, course)
                if survey.status == 3:
                    return current_user.ViewSurveyResults(survey, course)
        return ListSurveys.show_list()

class LoadSurvey:
    'loads a specific survey'
    def load(surveyID=None):
        if LoadSurvey.err_check():
            survey = Survey.query.filter_by(id=surveyID).first()    
            return survey
        return None

    def err_check():
        if (request.form.getlist("surveyid") == []):
            errorMSG("routes.opensurvey", "surveyid not selected")
            return False
        return True
        