# generic authentication check
if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))


class SecCheck(object):
    'purpose: implement generic runtime security checks'

    def authCheck(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))