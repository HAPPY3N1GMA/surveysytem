    def addqsurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin' and current_user.role != 'Staff'):
            common.Debug.errorMSG("routes.addqsurvey", "unauthorised user attempted access:",
                     current_user.id)
            return render_template("home.html", user=current_user)

        # get list of questions to add
        survey_questions = request.form.getlist('question')

        if survey_questions == []:
            common.Debug.errorMSG("routes.addqsurvey", "no questions selected")
            flash('No questions added to Survey')
            return survey_usage.OpenSurvey().open_attempt()	

        if (request.form.getlist("surveyid") == []):
            common.Debug.errorMSG("routes.addqsurvey", "surveyid not selected")
            return self.surveyinfo()

        surveyID = request.form["surveyid"]

        survey = surveys_model.Survey.query.filter_by(id=surveyID).first()	
        if(survey == None):
            common.Debug.errorMSG("routes.addqsurvey", "survey object is empty")
            return self.surveyinfo()	

        # check this staff member is authorised to add to this survey
        # check that they are authorised to add the type of question

        # this sorts and stores the questions into the survey
        for question in survey_questions:
            if (question[1:2]=='0'):	
                question = questions_model.MCQuestion.query.filter_by(id=int(question[4:5])).first()
                survey.mc_questions.append(question)
            elif (question[1:2]=='1'):
                question = questions_model.GeneralQuestion.query.filter_by(id=int(question[4:5])).first()
                survey.gen_questions.append(question)

        db_session.commit()

        # reload page
        return survey_usage.OpenSurvey().open_attempt()	