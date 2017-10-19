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

    def admin_load(self):
        admin = users_model.Admin(1, '1', 'Admin', [], [])
        db_session.add(admin)
        admin.courses = courses_model.Course.query.all()
        db_session.commit()
        print('Admin loaded...')

    def user_load(self):
        csv_in = open('passwords.csv', 'r')
        reader = csv.reader(csv_in)
        for row in reader:
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
                u.courses.append(course)

        db_session.commit()
        # q_users = db_session.query(users_model.UniUser).all()
        # for user in q_users:
        #     print(user)
        print ('Database load complete - starting app...')
