from sqlalchemy import Integer, ForeignKey, String, Column, Date
from sqlalchemy.orm import relationship
from database import Base


class UniUser(Base):
    __tablename__ = 'uniuser'
    id = Column(Integer,  primary_key=True)
    password = Column(String)
    role = Column(String)
    courses = relationship("Course", uselist=True)
    surveys = relationship("Survey", uselist=True)

    def __init__(self, id=None, password=None, role=None, courses=None,
                 surveys=None):
        self.id = id
        self.password = password
        self.role = role
        self.courses = courses
        self.surveys = surveys

    def __repr__(self):
        return '<UniUser %r>' % (self.name)


class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer,  primary_key=True)
    name = Column(String)
    password = Column(String)
    courses = relationship("Course", uselist=True)
    surveys = relationship("Survey", uselist=True)

    def __init__(self, name=None, password=None, role=None, courses=None,
                 surveys=None):
        self.name = name
        self.password = password
        self.role = role
        self.courses = courses
        self.surveys = surveys

    def __repr__(self):
        return '<User %r>' % (self.name)


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer,  primary_key=True)
    name = Column(String)
    password = Column(String)
    courses = relationship("Course", uselist=True)

    def __init__(self, name=None, password=None, role=None, courses=None):
        self.name = name
        self.password = password
        self.role = role
        self.courses = courses

    def __repr__(self):
        return '<User %r>' % (self.name)


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer,  primary_key=True)
    name = Column(String)
    password = Column(String)

    def __init__(self, name=None, password=None, role=None, courses=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<Admin %r>' % (self.name)


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    offering = Column(String)
    student_id = Column(Integer, ForeignKey('student.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))
    uniuser_id = Column(Integer, ForeignKey('uniuser.id'))

    def __init__(self, name=None, password=None, offeringid=None):
        self.name = name
        self.offering_id = offeringid

    def __repr__(self):
        return '<CourseName %r>' % (self.name)


# class Offering(Base):
#     __tablename__ = 'offering'
#     id = Column(Integer, primary_key=True)
#     semester = Column(Integer)
#     year = Column(Integer)

#     courses = relationship("Course", backref='offering', uselist=True)

#     def __init__(self, semester=None, year=None):
#         self.semester = semester
#         self.year = year

#     def __repr__(self):
#         return '<Offering Semester %r %r>' % (self.semester, self.year)


class MCQuestion(Base):
    __tablename__ = 'mcquestion'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answerOne = Column(String)
    answerTwo = Column(String)
    answerThree = Column(String)
    answerFour = Column(String)

    survey_id = Column(Integer, ForeignKey('survey.id'))

    def __init__(self, question=None, answerOne=None, answerTwo=None, 
                 answerThree=None, answerFour=None):
        self.question = question
        self.answerOne = answerOne
        self.answerTwo = answerTwo
        self.answerThree = answerThree
        self.answerFour = answerFour

    def __repr__(self):
        return '<MCQuestion %r>' % (self.question)    


#  Can be used for free text and yes/no q's
class GeneralQuestion(Base):
    __tablename__ = 'generalquestion'
    id = Column(Integer, primary_key=True)
    question = Column(String)

    survey_id = Column(Integer, ForeignKey('survey.id'))

    def __init__(self, question=None):
        self.question = question

    def __repr__(self):
        return '<General Question %r>' % (self.question)    


class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    course_id = Column(Integer, ForeignKey('course.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))
    uniuser_id = Column(Integer, ForeignKey('uniuser.id'))

    mc_questions = relationship("MCQuestion", uselist=True)
    gen_questions = relationship("GeneralQuestion", uselist=True)



    def __init__(self, title=None, date=None, course_id=None, 
                 mc_questions=None, gen_questions=None):
        self.title = title
        self.date = date
        self.course_id = course_id
        self.mc_questions = mc_questions
        self.gen_questions = gen_questions
        self.course_id = None
        self.staff_id = None

    def __repr__(self):
        return '<Survey %r>' % (self.title)  


# # How to store reponses in db?
# class Response(Base):
#     __tablename__ = 'response'
#     id = Column(Integer, primary_key=True)

