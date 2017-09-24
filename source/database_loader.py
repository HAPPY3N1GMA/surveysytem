import csv
from models import UniUser
from database import db_session


def user_load():
    with open('passwords.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        empty = []
        for row in reader:
            new = UniUser(row[0], row[1], row[2], [], [])
            db_session.add(new)

        db_session.commit()    
        users = UniUser.query.all()

        for user in users:
            print (user.id, user.password, user.role)