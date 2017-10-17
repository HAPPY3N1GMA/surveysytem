    def opensurvey(self):
        if (current_user.is_authenticated) == False:
            return redirect(url_for("login"))





        if (request.form.getlist("surveyid") == []):
            errorMSG("routes.opensurvey", "surveyid not selected")
            return self.surveyinfo()

        surveyID = request.form["surveyid"]

        survey = Survey.query.filter_by(id=surveyID).first()

        if(survey == None):
            errorMSG("routes.opensurvey", "survey object is empty")
            return self.surveyinfo()	

        course = Course.query.filter_by(id=survey.course_id).first()	


        if(course == None):
            errorMSG("routes.opensurvey","course object is empty")
            return self.surveyinfo()






            # todo: check if student answered survey already here looking at survey.uniuser_id!
            if survey.status == 2:
                return render_template("answersurvey.html", survey=survey,
                                       course=course)
            if survey.status == 3:
                #open survey results
                return self.selfsurveyinfo()

            return self.surveyinfo()

        if current_user in survey.users:

            general = GeneralQuestion.query.all()
            multi = MCQuestion.query.all()

            surveygen = survey.gen_questions
            surveymc = survey.mc_questions

            return render_template("modifysurvey.html",user=current_user,surveygen=surveygen,surveymc=surveymc,survey=survey,course=course,general=general,multi=multi)

        return self.surveyinfo()