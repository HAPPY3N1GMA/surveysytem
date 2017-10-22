import csv
from datetime import datetime, timedelta
#from models import users_model.UniUser, courses_model.Course
from models import users_model, courses_model
from database import db_session


class DB_Loader(object):

    def db_load(self):
        self.course_load()
        self.user_load()
        self.enrolment_load()
        self.admin_load()
        print ('Database load complete - starting app...')

    def admin_load(self):
        if users_model.UniUser.query.filter_by(id=1).first() is None:   
            admin = users_model.Admin(1, '1', 'Admin', [], [])
            db_session.add(admin)
            admin.courses = courses_model.Course.query.all()
            db_session.commit()
        print('Admin loaded...')

    def user_load(self):
        csv_in = open('passwords.csv', 'r')
        reader = csv.reader(csv_in)
        for row in reader:
            if users_model.UniUser.query.filter_by(id=row[0]).first() is None:  
                new = users_model.UniUser(row[0], row[1], row[2].capitalize(), [], [])
                db_session.add(new)
        db_session.commit()
        print('Users loaded...')
        # users = users_model.UniUser.query.all()
        # for user in users:
        #     print (user)

    def course_load(self):
        with open('courses.csv', 'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                if courses_model.Course.query.filter_by(name=row[0],offering=row[1]).first() is None:  
                    new = courses_model.Course(row[0], row[1])
                    db_session.add(new)
        db_session.commit()
        print ('Courses loaded...')

    def enrolment_load(self):
        with open('enrolments.csv', 'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                course = courses_model.Course.query.filter_by(offering=row[2]).\
                    filter_by(name=row[1]).first()
                u = db_session.query(users_model.UniUser).get(row[0])
                if course not in u.courses:
                    u.courses.append(course)
                    if course.survey:
                        for survey in course.survey:
                            survey.users.append(u)

        db_session.commit()
        print ('Users Enrolled and added to any Surveys')
        # q_users = db_session.query(users_model.UniUser).all()
        # for user in q_users:
        #     print(user)
        
