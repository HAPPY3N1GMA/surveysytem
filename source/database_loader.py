import csv
from models import UniUser, Course
from database import db_session


def db_load():
    admin_load()
    course_load()
    user_load()
    enrolment_load()


def admin_load():
    admin = UniUser(1111111, 'password', 'admin', [], [])
    db_session.add(admin)
    db_session.commit()


def user_load():
    csv_in = open('passwords.csv', 'r')
    reader = csv.reader(csv_in)
    for row in reader:
        new = UniUser(row[0], row[1], row[2], [], [])
        db_session.add(new)
    db_session.commit()
    # users = UniUser.query.all()
    # for user in users:
    #     print (user)


def course_load():
    with open('courses.csv', 'r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            new = Course(row[0], row[1])
            db_session.add(new)
    db_session.commit()


def enrolment_load():
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
