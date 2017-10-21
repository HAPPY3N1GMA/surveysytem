
    def answersurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        print("attempting to answer survey")

        #this is tempn
        if current_user.role != 'Student':
            if current_user.role != 'Guest':
                common.Debug.errorMSG("routes.answersurvey","unauthorised user attempted access:",current_user.id)
                return render_template("home.html", user=current_user)

        #check student answered all fields
        surveyID = request.form["surveyid"]

        survey = surveys_model.Survey.query.filter_by(id=surveyID).first()	
        if(survey==None):
            common.Debug.errorMSG("routes.answersurvey","survey object is empty")
            return self.surveyinfo()	

        #check user is in survey list
        if current_user not in survey.users:
            return render_template("home.html", user=current_user)

        course = courses_model.Course.query.filter_by(id=survey.course_id).first()	
        if(course==None):
            common.Debug.errorMSG("routes.answersurvey","course object is empty")
            return self.surveyinfo()

        genResponseList = []
        if len(survey.gen_questions)>0:

            genResponseList = request.form.getlist('genResponse')
            genResponseList = list(filter(None, genResponseList))

            if len(survey.gen_questions)!=len(genResponseList):
                common.Debug.errorMSG("routes.answersurvey","Extended Response Questions not completed")
                flash('Please Complete All Extended Response Questions')
                return survey_usage.OpenSurvey().open_attempt()	

        for text in genResponseList:
            if (get.cleanString(str(text))==False):
                common.Debug.errorMSG("routes.answersurvey","Invalid input in extended response")
                flash('Invalid Characters Used In Extended Response')
                return survey_usage.OpenSurvey().open_attempt()	


        mcResponseList = []
        if len(survey.mc_questions)>0:
            for question in survey.mc_questions:
                if (request.form.getlist(str(question.id))==[]):
                    common.Debug.errorMSG("routes.answersurvey","MultiChoice Questions not completed")
                    flash('Please Complete All Multiple Choice Questions')
                    return survey_usage.OpenSurvey().open_attempt()	

                mcResponseList.append(request.form[str(question.id)])

        mcResponseList = list(filter(None, mcResponseList))

        if len(survey.mc_questions)!=len(mcResponseList):
            common.Debug.errorMSG("routes.answersurvey","MultiChoice Questions not completed")
            flash('Please Complete All Multiple Choice Questions')
            return survey_usage.OpenSurvey().open_attempt()	


        #double check this person has not already responded? 

        surveyResponse = surveys_model.SurveyResponse(survey.id)
        db_session.add(surveyResponse)


        #this sorts and stores the answers into the survey response based on type
        for question,response in zip(survey.gen_questions,genResponseList):
            response = questions_model.GeneralResponse(surveyResponse.id,question.id,response)
            surveyResponse.gen_responses.append(response)

        for question,response in zip(survey.mc_questions,mcResponseList):
            response = questions_model.MCResponse(surveyResponse.id,question.id,response)
            surveyResponse.mc_responses.append(response)


        #remove the student from the survey list (so they cannont answer again)
        survey.users.remove(current_user)

        #commit the new survey response to this survey
        db_session.commit()

        #TODO: set survey to completed by this student to prevent resubmission!

        return redirect(url_for("submit"))
