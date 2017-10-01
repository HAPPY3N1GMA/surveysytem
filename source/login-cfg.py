from flask_login import LoginManager
from models import UniUser


class LoginConfig(object):

    def __init__(self):
        self.login_manager = LoginManager()

    def LoginConfig(self, app):
        # login_manager = LoginManager()
        self.login_manager.init_app(app)
        self.login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(userid):
        return UniUser(userid)