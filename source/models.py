from sqlalchemy import Integer, ForeignKey, String, Column, Date, Table
from sqlalchemy.orm import relationship
from database import Base
import ast


class UniUser(Base):
    __tablename__ = 'uniuser'
    id = Column(Integer,  primary_key=True)
    password = Column(String)
    role = Column(String)
    courses = relationship("Course",
                           secondary="ucassociation",
                           backref='uniuser')

    surveys = relationship("Survey", backref='uniuser')

    def __init__(self, id, password, role, courses=[],
                 surveys=[]):
        self.id = id
        self.password = password
        self.role = role
        self.courses = courses
        self.surveys = surveys

    def __repr__(self):
        return '<UniUser Id: %r, Courses: %r>' % (self.id, self.courses)


ucassociation_table = Table('ucassociation', Base.metadata,
                            Column('uniuser_id', Integer,
                                   ForeignKey('uniuser.id')),
                            Column('course_id', Integer,
                                   ForeignKey('course.id'))
                            )


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    offering = Column(String)
    uniusers = relationship("UniUser",
                            secondary="ucassociation",
                            backref="course")

    def __init__(self, name=None, offeringid=None, uniuserid=None):
        self.cid = id
        self.name = name
        self.offering = offeringid
        self.uniuser_id = uniuserid

    def __repr__(self):
        return '<CourseName %r>' % (self.name)



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



class QuestionResponse(Base):
    __tablename__ = 'questionresponse'
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer, ForeignKey('surveyresponse.id'))
    mcquestion_id = Column(Integer, ForeignKey('mcquestion.id'))
    genquestion_id = Column(Integer, ForeignKey('generalquestion.id'))
    response = Column(String)

    def __init__(self, responseid=None, mcquestionid=None, genquestionid=None,
                 _response=None):
        self.response_id = responseid
        self.mcquestion_id = mcquestionid
        self.genquestion_id = genquestionid
        self.response = _response

    def __repr__(self):
        return '<Response to %r or %r for %r>' % (self.question_id,
                                                  self.genquestion_id,
                                                  self.response_id)









#HOW TO LINK PEOPLE WHO CAN USE THIS SURVEY? it should be automatically
#done based on the course - as only course staff can access it!



class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    title = Column(String)
    date = Column(Date)
    course_id = Column(Integer, ForeignKey('course.id'))
    uniuser_id = Column(Integer, ForeignKey('uniuser.id'))

    mc_questions = relationship("MCQuestion",
                                secondary="mcassociation",
                                backref='survey')
    gen_questions = relationship("GeneralQuestion",
                                 secondary="genassociation",
                                 backref='survey')

    staff = relationship("UniUser", secondary="usassociation",
                         backref="survey")

    def __init__(self, title=None, date=None, courseid=None,
                 mcquestions=[], genquestions=[], _staff=[], status=1):
        self.title = title
        self.date = date
        self.course_id = courseid
        self.mc_questions = mcquestions
        self.gen_questions = genquestions
        self.staff = _staff
        self.status = status #1=open for edit, 2=open to answer, closed to edit, 3=closed

    def __repr__(self):
        return '<Survey %r>' % (self.title)  


class SurveyResponse(Base):
    __tablename__ = 'surveyresponse'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    responses = relationship("QuestionResponse",
                             backref="surveyresponse")

    def __init__(self, surveyid=None, _responses=None):
        self.survey_id = surveyid
        self.responses = _responses

    def __repr__(self):
        return '<Response to %r>' % (self.survey_id)       







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

genassociation_table = Table('genassociation', Base.metadata,
                             Column('generalquestion_id', Integer,
                                    ForeignKey('generalquestion.id')),
                             Column('survey_id', Integer,
                                    ForeignKey('survey.id'))
                             )

