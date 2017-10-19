from sqlalchemy import Integer, ForeignKey, String, Column, Date, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base, db_session
from datetime import datetime
import ast
from flask_login import current_user
from abc import ABCMeta, abstractmethod
from flask import Flask, redirect, render_template, request, url_for, flash
from classes import common

from models import surveys_model, questions_model, courses_model


class UniUser(Base):
    __tablename__ = 'uniuser'
    id = Column(Integer,  primary_key=True)
    password = Column(String)
    role = Column(String)
    courses = relationship("courses_model.Course",
                           secondary="ucassociation",
                           backref='uniuser')

    #surveys = relationship("surveys_model.Survey", backref='uniuser')

    surveys = relationship("surveys_model.Survey",
                           secondary="usassociation",
                           backref='uniuser')

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __init__(self, id, password, role, courses=[],
                 surveys=[]):
        self.id = id
        self.password = password
        self.role = role
        self.courses = courses
        self.surveys = surveys

    def get_staff():
        staff = UniUser.query.filter_by(role='Staff').all() 
        if(staff==None):
            print("get_staff","staff object list is empty")
            return False
        return staff

    def get_students():
        students = UniUser.query.filter_by(role='Student').all() 
        if(students==None):
            print("get_students","staff object list is empty")
            return False
        return students

    def is_enrolled(self,course):
        if course in self.courses:
            return True
        return False

    def __repr__(self):
        return '<UniUser Id: %r, Courses: %r>' % (self.id, self.courses)

    @abstractmethod
    def CreateSurvey(self,courseId,surveyName,startDate,endDate):
        pass

    @abstractmethod
    def AnswerSurvey(self,survey,course):
        pass

    @abstractmethod
    def ModifySurvey(self,survey,course): 
        pass

    @abstractmethod
    def ViewSurveyResults(self,survey):
        pass

    @abstractmethod
    def PushSurvey(self,survey,course): 
        pass

    @abstractmethod
    def EndSurvey(self,survey,course): 
        pass

    @abstractmethod
    def PublishSurvey(self,survey,course): 
        pass


    __mapper_args__ = {
        'polymorphic_on':role,
        'polymorphic_identity':'uniuser'
    }



class Admin(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Admin'
    }


    def CreateSurvey(self,courseId,surveyName,startDate,endDate):

        survey = surveys_model.Survey(surveyName, courseId)
        survey.set_dates(startDate,endDate)

        course = courses_model.Course.query.filter_by(id=courseId).first() 
        course.survey.append(survey)

        current_user.survey.append(survey)

        db_session.add(survey)
        db_session.commit()

        return common.Render.surveys()


    def AnswerSurvey(self,survey,course):
        # run code for answering if applicable
        return current_user.ModifySurvey(survey, course)


    def ModifySurvey(self,survey,course):
        # run code for modifying if applicable
        general = questions_model.GeneralQuestion.query.all()
        multi = questions_model.MCQuestion.query.all()

        surveygen = survey.gen_questions
        surveymc = survey.mc_questions

        return common.Render.modify_survey(surveygen,surveymc,survey,course,general,multi)


    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        flash('model.py - Admin will get redirected to survey results page')
        return common.Render.surveys()


    def PushSurvey(self,survey,course):       
        'Update survey status to editable by staff members'
        if survey.add_staff():
            survey.status = 1
            db_session.commit()
        else:
            flash("Error Adding Staff to surveys_model.Survey")
        return current_user.ModifySurvey(survey, course)


    def PublishSurvey(self,survey,course): 
        if survey.mc_questions == [] and survey.gen_questions == []:
            flash('No questions added to surveys_model.Survey')
        elif survey.add_students() == False:
            flash('Error Adding Students to surveys_model.Survey')
        else:
            survey.status = 2
            db_session.commit()

        return current_user.ModifySurvey(survey, course)


    def EndSurvey(self,survey,course): 
        survey.status = 3
        db_session.commit()
        return current_user.ModifySurvey(survey, course)





class Staff(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Staff'
    }

    def CreateSurvey(self,courseId,surveyName,startDate,endDate):
        return common.Render.home()


    def AnswerSurvey(self,survey,course):
        return current_user.ModifySurvey(survey, course)


    def ModifySurvey(self,survey,course):
        general = questions_model.GeneralQuestion.query.all()
        multi = questions_model.MCQuestion.query.all()

        surveygen = survey.gen_questions
        surveymc = survey.mc_questions

        return common.Render.modify_survey(surveygen,surveymc,survey,course,general,multi)


    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        flash('model.py - Staff will get redirected to survey results page')
        return common.Render.surveys()


    def PushSurvey(self,survey,course): 
        common.Debug.errorMSG("routes.statussurvey","unauthorised user attempted access:",current_user.id)
        return common.Render.home()


    def EndSurvey(self,survey,course): 
        survey.status = 3
        db_session.commit()
        return current_user.ModifySurvey(survey, course)


    def PublishSurvey(self,survey,course): 

        if survey.mc_questions == [] and survey.gen_questions == []:
            flash('No questions added to surveys_model.Survey')
        elif survey.add_students() == False:
            flash('Error Adding Students to surveys_model.Survey')
        else:
            survey.status = 2
            db_session.commit()

        return current_user.ModifySurvey(survey, course)


class Student(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Student'
    }

    def CreateSurvey(self,courseId,surveyName,startDate,endDate):
        return common.Render.home()


    def AnswerSurvey(self,survey,course):
        # run code for answering if applicable
        return render_template("answersurvey.html", survey=survey,
                                       course=course)

    def ModifySurvey(self,survey,course):
        return common.Render.home()


    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        flash('model.py - Student will get redirected to survey results page')
        return common.Render.surveys()


    def PushSurvey(self,survey,course): 
        return common.Render.home()


    def PublishSurvey(self,survey,course): 
        return common.Render.home()        


    def EndSurvey(self,survey,course): 
        return common.Render.home()





class Guest(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Guest'
    }

    def CreateSurvey(self,courseId,surveyName,startDate,endDate):
        return common.Render.home()


    def AnswerSurvey(self,survey,course):
        # run code for answering if applicable
        return render_template("answersurvey.html", survey=survey,
                                       course=course)

    def ModifySurvey(self,survey,course):
        return common.Render.home()


    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        flash('model.py - Guest will get redirected to survey results page')
        return common.Render.surveys()


    def PushSurvey(self,survey,course): 
        return common.Render.home()


    def PublishSurvey(self,survey,course): 
        return common.Render.home()        


    def EndSurvey(self,survey,course): 
        return common.Render.home()





