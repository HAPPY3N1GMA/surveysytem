

    def removeqsurvey(self):
        if (current_user.is_authenticated) == False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin' and current_user.role != 'Staff'):
            common.Debug.errorMSG("routes.removeqsurvey",
                     "unauthorised user attempted access:",
                     current_user.id)
            return render_template("home.html", user=current_user)

        if request.form.getlist('question')==[]:
            common.Debug.errorMSG("routes.removeqsurvey","no questions selected")
            return survey_usage.OpenSurvey().open_attempt()	

        survey_question = request.form['question']

        if (request.form.getlist("surveyid")==[]):
            common.Debug.errorMSG("routes.removeqsurvey","surveyid not selected")
            return self.surveyinfo()

        surveyID = request.form["surveyid"]
        survey = surveys_model.Survey.query.filter_by(id=surveyID).first()	
        if(survey == None):
            common.Debug.errorMSG("routes.removeqsurvey","survey object is empty")
            return self.surveyinfo()	

        # remove question from the survey
        if (survey_question[1:2] == '0'):
            question = questions_model.MCQuestion.query.filter_by(id=int(survey_question[4:5])).first()
            survey.mc_questions.remove(question)
        elif (survey_question[1:2]=='1'):
            question = questions_model.GeneralQuestion.query.filter_by(id=int(survey_question[4:5])).first()
            survey.gen_questions.remove(question)

        db_session.commit()

        return survey_usage.OpenSurvey().open_attempt()	