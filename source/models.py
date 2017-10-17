from sqlalchemy import Integer, ForeignKey, String, Column, Date, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base, db_session
from datetime import datetime
import ast
from flask_login import current_user
from abc import ABCMeta, abstractmethod
from flask import Flask, redirect, render_template, request, url_for, flash

class UniUser(Base):
    __tablename__ = 'uniuser'
    id = Column(Integer,  primary_key=True)
    password = Column(String)
    role = Column(String)
    courses = relationship("Course",
                           secondary="ucassociation",
                           backref='uniuser')

    #surveys = relationship("Survey", backref='uniuser')

    surveys = relationship("Survey",
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
        staff = UniUser.query.filter_by(role='staff').all() 
        if(staff==None):
            print("get_staff","staff object list is empty")
            return False
        return staff

    def get_students():
        students = UniUser.query.filter_by(role='student').all() 
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
    def AnswerSurvey(self,survey,course):
        pass

    @abstractmethod
    def ModifySurvey(self,survey,course):
        print("ERRRRROOOORRRR")
        pass

    @abstractmethod
    def ViewSurveyResults(self,survey,course):
        pass

    __mapper_args__ = {
        'polymorphic_on':role,
        'polymorphic_identity':'uniuser'
    }

class Admin(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Admin'
    }

    def AnswerSurvey(self,survey,course):
        # run code for answering if applicable
        return  ListSurveys.show_list()

    def ModifySurvey(self,survey,course):
        # run code for modifying if applicable
        print("1",course)
        general = GeneralQuestion.query.all()
        multi = MCQuestion.query.all()

        surveygen = survey.gen_questions
        surveymc = survey.mc_questions

        return render_template("modifysurvey.html",user=current_user,
            surveygen=surveygen,surveymc=surveymc,survey=survey,
            course=course,general=general,multi=multi)

    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        return  ListSurveys.show_list() # TODO impl

class Staff(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Staff'
    }

    def AnswerSurvey(self,survey,course):
        # run code for answering if applicable
        return  ListSurveys.show_list()

    def ModifySurvey(self,survey,course):
        # run code for modifying if applicable
        general = GeneralQuestion.query.all()
        multi = MCQuestion.query.all()

        surveygen = survey.gen_questions
        surveymc = survey.mc_questions

        return render_template("modifysurvey.html",user=current_user,
            surveygen=surveygen,surveymc=surveymc,survey=survey,
            course=course,general=general,multi=multi)


    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        return  ListSurveys.show_list()

class Student(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Student'
    }

    def AnswerSurvey(self,survey,course):
        # run code for answering if applicable
        return render_template("answersurvey.html", survey=survey,
                                       course=course)

    def ModifySurvey(self,survey,course):
        # run code for modifying if applicable
        return  ListSurveys.show_list()

    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        return  ListSurveys.show_list()

class Guest(UniUser):

    __mapper_args__ = {
        'polymorphic_identity':'Guest'
    }

    def AnswerSurvey(self,survey,course):
        # run code for answering if applicable
        return render_template("answersurvey.html", survey=survey,
                                       course=course)

    def ModifySurvey(self,survey,course):
        # run code for modifying if applicable
        return  ListSurveys.show_list()

    def ViewSurveyResults(self,survey,course):
        # run code for viewing results if applicable
        return  ListSurveys.show_list()
















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



#question status
# 0 = Standard
# 1 = Optional
# 3 = Deleted



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
        return '<GeneralResponse to %r or %r for %r>' % (self.question_id,
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
        return '<MCResponse to %r or %r for %r>' % (self.question_id,
                                                  self.response_id)



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
        current_time = datetime.now()
        if self.date_start > current_time and self.date_end < current_time:
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

    #uniuser_id = Column(Integer, ForeignKey('uniuser.id'))

    mc_questions = relationship("MCQuestion",
                                secondary="mcassociation",
                                backref='survey')
    gen_questions = relationship("GeneralQuestion",
                                 secondary="genassociation",
                                 backref='survey')
    #what users have accesss to this survey (both students and staff - can remove students then)
    users = relationship("UniUser", secondary="usassociation",
                         backref="survey")


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


    def get_course(self):
        course = Course.query.filter_by(id=self.course_id).first()    
        if(course==None):
            print("get_course","course object is empty")
        return course

    def add_staff(self):
        course = self.get_course()
        staff = UniUser.get_staff()
        return self.add_users(staff,course)

    def add_students(self):
        course = self.get_course()
        students = UniUser.get_students()
        return self.add_users(students,course)

    def add_users(self,userList=[],course=None):
        if userList == []:
            print("add_users","userList is empty")
            return False
        if course == None:
            print("add_users","course is empty")
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
        return '<Response to %r>' % (self.survey_id)       






ucassociation_table = Table('ucassociation', Base.metadata,
                            Column('uniuser_id', Integer,
                                   ForeignKey('uniuser.id')),
                            Column('course_id', Integer,
                                   ForeignKey('course.id'))
                            )




usassociation_table = Table('usassociation', Base.metadata,
                            Column('uniuser_id', Integer,
                                   ForeignKey('uniuser.id')),
                            Column('survey_id', Integer,
                                   ForeignKey('survey.id'))
                            )


mcassociation_table = Table('mcassociation', Base.metadata,
                            Column('mcquestion_id', Integer,
                                   ForeignKey('mcquestion.id')),
                            Column('survey_id', Integer,
                                   ForeignKey('survey.id'))
                            )

"""ynassociation_table = Table('ynassociation', Base.metadata,
                            Column('ynquestion_id', Integer,
                                   ForeignKey('ynquestion.id')),
                            Column('survey_id', Integer,
                                   ForeignKey('survey.id'))
                            )"""

genassociation_table = Table('genassociation', Base.metadata,
                             Column('generalquestion_id', Integer,
                                    ForeignKey('generalquestion.id')),
                             Column('survey_id', Integer,
                                    ForeignKey('survey.id'))
                             )

