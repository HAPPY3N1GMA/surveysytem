from sqlalchemy import Integer, ForeignKey, String, Column, Date, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base, db_session
from datetime import datetime
import ast
from flask_login import current_user
from abc import ABCMeta, abstractmethod
from flask import Flask, redirect, render_template, request, url_for, flash
from classes import common



class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    offering = Column(String)
    uniusers = relationship("UniUser",
                            secondary="ucassociation",
                            backref="course")
    #survey_id = Column(Integer, ForeignKey('survey.id'))

    survey = relationship("Survey",
                       secondary="csassociation",
                       backref='course')

    def __init__(self, name=None, offeringid=None, survey=[]):
        self.name = name
        self.offering = offeringid
        self.survey = survey
        #self.uniuser_id = uniuserid

    def __repr__(self):
        return '<CourseName %r>' % (self.name)

csassociation_table = Table('csassociation', Base.metadata,
                            Column('course_id', Integer,
                                   ForeignKey('course.id')),
                            Column('survey_id', Integer,
                                   ForeignKey('survey.id'))
                            )

