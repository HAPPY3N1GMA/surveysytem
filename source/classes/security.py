from flask_login import login_user, login_required, current_user, logout_user
from flask import Flask, redirect, render_template, request, url_for, flash

class SecChecks(object):
    'purpose: implement generic runtime security checks'

    def authCheck(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))