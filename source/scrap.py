def questioninfo(self):
        # standard security authentication check
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.questioninfo","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        #read in list of questions from db, filter out any not available to user or deleted
        general = questions_model.GeneralQuestion.query.all()
        multi = questions_model.MCQuestion.query.all()
        return render_template("questions.html",user=current_user,multi=multi,general=general)

##############################################################

        

        general = questions_model.GeneralQuestion.query.all()
        multi = questions_model.MCQuestion.query.all()

