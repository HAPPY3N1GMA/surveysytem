from sqlalchemy import Integer, ForeignKey, String, Column, Date,\
 Table, Boolean
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

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

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
        self.name = name
        self.offering = offeringid
        self.uniuser_id = uniuserid

    def __repr__(self):
        return '<CourseName %r>' % (self.name)


class MCQuestion(Base):
    __tablename__ = 'mcquestion'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answerOne = Column(String)
    answerTwo = Column(String)
    answerThree = Column(String)
    answerFour = Column(String)

    # If false, question is mandatory
    # Boolean in SQLite are not True/False
    # Stored as 1 for True, 0 False
    optional = Column(Boolean)

    surveys = relationship("Survey",
                           secondary="mcassociation",
                           backref="mcquestion")

    def __init__(self, question=None, answerOne=None, answerTwo=None, 
                 answerThree=None, answerFour=None):
        self.question = question
        self.answerOne = answerOne
        self.answerTwo = answerTwo
        self.answerThree = answerThree
        self.answerFour = answerFour

    def __repr__(self):
        questionAnswers = str([self.answerOne, self.answerTwo, 
                              self.answerThree, self.answerFour])
        questionAnswers = ast.literal_eval(str(questionAnswers))
        return str([self.question,questionAnswers])


      #  return ('[%r, "[%r, %r, %r, %r]"]' % (self.question,
      #                 self.answerOne,
      #                 self.answerTwo,
      #                 self.answerThree,
      #                 self.answerFour))

      #original
      #def __repr__(self):
      #  return '<MCQuestion %r>' % (self.question)


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


#  Can be used for free text 
class GeneralQuestion(Base):
    __tablename__ = 'generalquestion'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    # If false, question is mandatory
    # Boolean in SQLite are not True/False
    # Stored as 1 for True, 0 False
    optional = Column(Boolean)

    surveys = relationship("Survey",
                           secondary="genassociation",
                           backref="generalquestion")

    def __init__(self, question=None):
        self.question = question

    #def __repr__(self):
    #    return '<General Question %r>' % (self.question)    

    def __repr__(self):
        return '%r' % (self.question)


class YNQuestion(Base):
    __tablename__ = 'ynquestion'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    # If false, question is mandatory
    # Boolean in SQLite are not True/False
    # Stored as 1 for True, 0 False
    optional = Column(Boolean)

    surveys = relationship("Survey",
                           secondary="ynassociation",
                           backref="ynquestion")

    def __init__(self, question=None):
        self.question = question

    #def __repr__(self):
    #    return '<General Question %r>' % (self.question)    

    def __repr__(self):
        return '%r - Yes/No' % (self.question)


class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
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
    gen_questions = relationship("YNQuestion",
                                 secondary="ynassociation",
                                 backref='survey')                             

    staff = relationship("UniUser", secondary="usassociation",
                         backref="survey")

    def __init__(self, title=None, date=None, courseid=None,
                 mcquestions=None, genquestions=None, _staff=None):
        self.title = title
        self.date = date
        self.course_id = courseid
        self.mc_questions = mcquestions
        self.gen_questions = genquestions
        self.staff = _staff

    def __repr__(self):
        return '<Survey %r>' % (self.title)  


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

ynassociation_table = Table('ynassociation', Base.metadata,
                            Column('ynquestion_id', Integer,
                                   ForeignKey('ynquestion.id')),
                            Column('survey_id', Integer,
                                   ForeignKey('survey.id'))
                            )
