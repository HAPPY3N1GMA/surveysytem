from sqlalchemy import Integer, ForeignKey, String, Column, Date, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base, db_session
from datetime import datetime
import ast
from flask_login import current_user
from abc import ABCMeta, abstractmethod
from flask import Flask, redirect, render_template, request, url_for, flash
from classes import common



#  Can be used for free text and yes/no q's
class GeneralQuestion(Base):
    __tablename__ = 'generalquestion'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    question = Column(String)

    surveys = relationship("Survey",
                           secondary="genassociation",
                           backref="generalquestion")

    def __init__(self, question=None, status=None):
        self.question = question
        self.status = status

    #def __repr__(self):
    #    return '<General Question %r>' % (self.question)    

    def __repr__(self):
        return  str([self.id,self.question,self.status])

    def removefromsurvey(self,survey):
        if self in survey.gen_questions:
          survey.gen_questions.remove(self)
          db_session.commit()

    def addtosurvey(self,survey):
          survey.gen_questions.append(self)
          db_session.commit()


class MCQuestion(Base):
    __tablename__ = 'mcquestion'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    question = Column(String)
    answerOne = Column(String)
    answerTwo = Column(String)
    answerThree = Column(String)
    answerFour = Column(String)

    surveys = relationship("Survey",
                           secondary="mcassociation",
                           backref="mcquestion")

    def __init__(self, question=None, answerOne=None, answerTwo=None, 
                 answerThree=None, answerFour=None, status=None):
        self.question = question
        self.answerOne = answerOne
        self.answerTwo = answerTwo
        self.answerThree = answerThree
        self.answerFour = answerFour
        self.status = status

    def __repr__(self):
        questionAnswers = str([self.answerOne, self.answerTwo, 
                              self.answerThree, self.answerFour])
        questionAnswers = ast.literal_eval(str(questionAnswers))
        return str([self.id,self.question,questionAnswers,self.status])


    def removefromsurvey(self,survey):
        if self in survey.mc_questions:
          survey.mc_questions.remove(self)
          db_session.commit()

    def addtosurvey(self,survey):
          survey.mc_questions.append(self)
          db_session.commit()




class GeneralResponse(Base):
    __tablename__ = 'generalresponse'
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey('surveyresponse.id'))
    question_id = Column(Integer, ForeignKey('generalquestion.id'))
    response = Column(String)

    def __init__(self, responseid=None, questionid=None,
                 _response=None):
        self.response_id = responseid
        self.question_id = questionid
        self.response = _response

    def __repr__(self):
        return '<MCResponse to %r is %r>' % (self.question_id,
                                             self.response_id)

class MCResponse(Base):
    __tablename__ = 'mcresponse'
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey('surveyresponse.id'))
    question_id = Column(Integer, ForeignKey('mcquestion.id'))
    response = Column(String)

    def __init__(self, responseid=None, questionid=None,
                 _response=None):
        self.response_id = responseid
        self.question_id = questionid
        self.response = _response

    def __repr__(self):
        return '<MCResponse to %r is %r>' % (self.question_id,
                                             self.response_id)



mcassociation_table = Table('mcassociation', Base.metadata,
                            Column('mcquestion_id', Integer,
                                   ForeignKey('mcquestion.id')),
                            Column('survey_id', Integer,
                                   ForeignKey('survey.id'))
                            )

genassociation_table = Table('genassociation', Base.metadata,
                             Column('generalquestion_id', Integer,
                                    ForeignKey('generalquestion.id')),
                             Column('survey_id', Integer,
                                    ForeignKey('survey.id'))
                             )
