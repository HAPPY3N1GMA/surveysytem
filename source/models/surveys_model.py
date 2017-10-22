from sqlalchemy import Integer, ForeignKey, String, Column, Date, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base, db_session
from datetime import datetime
import ast
from flask_login import current_user
from abc import ABCMeta, abstractmethod
from flask import Flask, redirect, render_template, request, url_for, flash
from classes import common

from models import courses_model, users_model, questions_model




#this is new and needs adding to diagrams
class SurveyDate(Base):
    __tablename__ = 'surveydate'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    survey = relationship("Survey", back_populates="date")
    date_created = Column(Date)
    date_start = Column(Date)
    date_end = Column(Date)

    def __init__(self, date_start=None, date_end = None):
        self.date_created = datetime.now()
        self.date_start = date_start
        self.date_end = date_end

    def is_active(self):
        """Return true if the survey is active."""

        current_time = datetime.date(datetime.today())
        if self.date_start < current_time and self.date_end > current_time:
            return True
        return False

    def is_expired(self):
        """Return true if the survey is active."""
        current_time = datetime.date(datetime.today())
        if self.date_end < current_time:
            return True
        return False

    def set_start(self,date=None):
        self.date_start = date
        db_session.commit()

    def set_end(self,date=None):
        self.date_end = date
        db_session.commit()


class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    title = Column(String)

    date = relationship("SurveyDate", uselist=False, back_populates="survey")

    course_id = Column(Integer, ForeignKey('course.id'))

    # uniuser_id = Column(Integer, ForeignKey('uniuser.id'))

    mc_questions = relationship("MCQuestion",
                                secondary="mcassociation",
                                backref='survey')
    gen_questions = relationship("GeneralQuestion",
                                 secondary="genassociation",
                                 backref='survey')
    #what users have accesss to this survey (both students and staff - can remove students then)
    users = relationship("users_model.UniUser", secondary="usassociation",
                         backref="survey")

    responses = relationship("SurveyResponse", backref='survey')


    def __init__(self, title=None, courseid=None, mcquestions=[], genquestions=[], 
                 _users=[], status=0):
        date = SurveyDate()
        db_session.add(date)
        #db_session.commit()

        self.title = title
        self.date = date
        self.course_id = courseid
        self.mc_questions = mcquestions
        self.gen_questions = genquestions
        self.users = _users
        self.status = status #1=open for edit, 2=open to answer, closed to edit, 3=closed

    def __repr__(self):
        return '<Survey %r>' % (self.title)  

    def status_check(self):
        if self.date.is_active():
            if self.status == 2:
                print("Starting Survey: ",self.title," - survey is now live!")
                if self.add_students() == False:
                    print('Error Adding Students to survey id:',self)
                self.status = 3
        elif self.date.is_expired():
            if self.status == 3:
                print("Ending Survey: ",self.title," - survey is now closed!")
                self.status = 4
        db_session.commit()        


    def get_course(self):
        course = courses_model.Course.query.filter_by(id=self.course_id).first()    
        if(course==None):
            print("get_course","course object is empty")
        return course

    def add_staff(self):
        course = self.get_course()
        staff = users_model.UniUser.get_staff()
        return self.add_users(staff,course)

    def add_students(self):
        course = self.get_course()
        students = users_model.UniUser.get_students()
        return self.add_users(students,course)

    def set_dates(self,startDate,endDate):
        self.date.set_start(startDate)
        self.date.set_end(endDate)

    def add_users(self,userList=[],course=None):
        if userList == []:
            return False
        if course == None:
            return False

        for user in userList:
            if user.is_enrolled(course):
                self.users.append(user)

        db_session.commit()
        return True


class SurveyResponse(Base):
    __tablename__ = 'surveyresponse'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    mc_responses = relationship("MCResponse",
                             backref="surveyresponse")
    gen_responses = relationship("GeneralResponse",
                             backref="surveyresponse")

    def __init__(self, surveyid=None, _mc_responses=[], _gen_responses=[]):
        self.survey_id = surveyid
        self.mc_responses = _mc_responses
        self.gen_responses = _gen_responses

    def __repr__(self):
        return '<Response to %r>' % (self.survey_id,
                                     )







usassociation_table = Table('usassociation', Base.metadata,
                            Column('uniuser_id', Integer,
                                   ForeignKey('uniuser.id')),
                            Column('survey_id', Integer,
                                   ForeignKey('survey.id'))
                            )



