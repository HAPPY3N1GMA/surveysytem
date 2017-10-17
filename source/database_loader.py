import csv
from models import UniUser, Course
from database import db_session


class DB_Loader(object):

    def db_load(self):
        self.course_load()
        self.user_load()
        self.enrolment_load()
        self.admin_load()

    def admin_load(self):
        admin = UniUser(1, '1', 'Admin', [], [])
        db_session.add(admin)
        admin.courses = Course.query.all()
        db_session.commit()
        print('Admin loaded...')

    def user_load(self):
        csv_in = open('passwords.csv', 'r')
        reader = csv.reader(csv_in)
        for row in reader:
            new = UniUser(row[0], row[1], row[2].capitalize(), [], [])
            db_session.add(new)
        db_session.commit()
        print('Users loaded...')
        # users = UniUser.query.all()
        # for user in users:
        #     print (user)

    def course_load(self):
        with open('courses.csv', 'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                new = Course(row[0], row[1])
                db_session.add(new)
        db_session.commit()
        print ('Courses loaded...')

    def enrolment_load(self):
        with open('enrolments.csv', 'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                course = Course.query.filter_by(offering=row[2]).\
                    filter_by(name=row[1]).first()
                u = db_session.query(UniUser).get(row[0])
                u.courses.append(course)

        db_session.commit()
        # q_users = db_session.query(UniUser).all()
        # for user in q_users:
        #     print(user)
        print ('Database load complete - starting app...')
