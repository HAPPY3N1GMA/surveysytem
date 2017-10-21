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

    def get_admin():
        admin = UniUser.query.filter_by(role='Admin').first() 
        if(admin==None):
            print("get_admin","admin object list is empty")
            return False
        return admin

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

    @abstractmethod
    def AddQuestionSurvey(self,survey_questions,survey,course):
        pass

    @abstractmethod
    def RemoveQuestionSurvey(self,survey_question,survey,course):
        pass

    @abstractmethod
    def OpenQuestions(self):
        pass

    __mapper_args__ = {
        'polymorphic_on':role,
        'polymorphic_identity':'uniuser'
    }

###############################################################################################

class Admin(UniUser):
    reg_requests = relationship("RegistrationRequest", backref='uniuser')

    def __init__(self, id, password, role, courses=[],
                 surveys=[],reg_requests=[]):
        print("creating an admin user")
        self.id = id
        self.password = password
        self.role = role
        self.courses = courses
        self.surveys = surveys
        self.reg_requests = reg_requests

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
        'Update survey status to answerable by students/guests'
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



    def AddQuestionSurvey(self,survey_questions,survey,course):
        'Add list of questions to the survey'
        print("adding")

        for question in survey_questions:
            question = ast.literal_eval(str(question))
            if (question[0]==0):  
                print("mc",question)  
                question = questions_model.MCQuestion.query.filter_by(id=int(question[1])).first()
                survey.mc_questions.append(question)
            elif (question[0]==1):
                print("gen",question)  
                question = questions_model.GeneralQuestion.query.filter_by(id=int(question[1])).first()
                survey.gen_questions.append(question)

        db_session.commit()

        return current_user.ModifySurvey(survey, course)


    def RemoveQuestionSurvey(self,survey_question,survey,course):
        'Remove a question from a survey'
        if (survey_question[0] == '0'):
            question = questions_model.MCQuestion.query.filter_by(id=int(survey_question[1])).first()
            survey.mc_questions.remove(question)
        elif (survey_question[0]=='1'):
            question = questions_model.GeneralQuestion.query.filter_by(id=int(survey_question[1])).first()
            survey.gen_questions.remove(question)

        db_session.commit()
        return current_user.ModifySurvey(survey, course)

    def OpenQuestions(self):
        general = questions_model.GeneralQuestion.query.all()
        multi = questions_model.MCQuestion.query.all()
        return render_template("questions.html",user=current_user,multi=multi,general=general)

###############################################################################################

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


    def AddQuestionSurvey(self,survey_questions,survey,course):
        'Add list of questions to the survey'
        print("adding")

        for question in survey_questions:
            question = ast.literal_eval(str(question))
            if (question[0]==0):  
                print("mc",question)  
                question = questions_model.MCQuestion.query.filter_by(id=int(question[1])).first()
                survey.mc_questions.append(question)
            elif (question[0]==1):
                print("gen",question)  
                question = questions_model.GeneralQuestion.query.filter_by(id=int(question[1])).first()
                survey.gen_questions.append(question)

        db_session.commit()

        return current_user.ModifySurvey(survey, course)


    def RemoveQuestionSurvey(self,survey_question,survey,course):
        'Remove a question from a survey'
        if (survey_question[0] == '0'):
            question = questions_model.MCQuestion.query.filter_by(id=int(survey_question[1])).first()
            survey.mc_questions.remove(question)
        elif (survey_question[0]=='1'):
            question = questions_model.GeneralQuestion.query.filter_by(id=int(survey_question[1])).first()
            survey.gen_questions.remove(question)

        db_session.commit()
        return current_user.ModifySurvey(survey, course)

    def OpenQuestions(self):
        common.Debug.errorMSG("routes.questioninfo","unauthorised user attempted access:",current_user.id)
        return render_template("home.html", user=current_user)

###############################################################################################

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


    def AddQuestionSurvey(self,survey_questions,survey,course):
        return common.Render.home()

    def RemoveQuestionSurvey(self,survey_question,survey,course):
        return common.Render.home()

    def OpenQuestions(self):
        common.Debug.errorMSG("routes.questioninfo","unauthorised user attempted access:",current_user.id)
        return render_template("home.html", user=current_user)

###############################################################################################

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


    def AddQuestionSurvey(self,survey_questions,survey,course):
        return common.Render.home()

    def RemoveQuestionSurvey(self,survey_question,survey,course):
        return common.Render.home()

    def OpenQuestions(self):
        common.Debug.errorMSG("routes.questioninfo","unauthorised user attempted access:",current_user.id)
        return render_template("home.html", user=current_user)

###############################################################################################

class RegistrationRequest(Base):
    __tablename__ = 'regrequest'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    password = Column(String)
    course_id = Column(Integer, ForeignKey('course.id'))
    admin = Column(Integer, ForeignKey('uniuser.id'))

    def __init__(self, userId=None, password="",
                 course_id=""):
        self.userId = userId
        self.password = password
        self.course_id = course_id

    def __repr__(self):
        return '<RegistrationRequest for %r and  %r>' % (self.userId,
                                             self.course_id)



