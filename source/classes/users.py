class User(object):
    def __init__(self, name, user_id, password, role):
        self._name = name
        self._user_id = user_id
        self._password = password
        self._role = role

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role


class Admin(User):
    def __init__(self, name, user_id, password, role):
        User.__init__(name, user_id, password, role)


class UniUser(User):
    def __init__(self, name, user_id, password, role, courses):
        User.__init__(name, user_id, password, role)
        self.courses = []

    def enrol_in_course(self, course):
        self.courses.append(course)

    def unenrol_in_course(self, course):
        self.courses.remove(course)

    def returnList(self):
        return self.courses


class Student(UniUser):
    def __init__(self, name, user_id, password, role, courses):
        UniUser.__init__(name, user_id, password, role)


class Staff(UniUser):
    def __init__(self, name, user_id, password, role, courses):
        UniUser.__init__(name, user_id, password, role)

