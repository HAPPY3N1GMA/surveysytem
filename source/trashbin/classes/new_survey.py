    def newsurvey(self):
        if (current_user.is_authenticated) == False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin'):
            errorMSG("routes.newsurvey", "unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        survey_name = request.form["svyname"]
        if survey_name == "":
            flash('Please Enter a Valid Survey Name')
            return self.surveyinfo()  

        courseID = request.form["svycourse"]
        startdate = request.form["startdate"]
        enddate = request.form["enddate"]

        try:
            startdate = datetime.strptime(startdate, '%Y/%m/%d')
            enddate = datetime.strptime(enddate, '%Y/%m/%d')
        except ValueError:
            errorMSG("routes.newsurvey", "Invalid Date Entered")  
            flash('Please Enter a Start and Finish Date')
            return self.surveyinfo()  
        


        #print("NEW COURSE ID:", courseID)

        course = Course.query.filter_by(id=courseID).first()	
        if(course == None):
            errorMSG("routes.newsurvey", "course object is empty")
            return self.surveyinfo()

        # Object=Course.query.filter_by(id=courseID).first()

        if (get.cleanString(str(survey_name)) == False):
            errorMSG("routes.newsurvey", "Invalid Characters in survey name")
            return self.surveyinfo()

        if (str(courseID) == ''):
            errorMSG("routes.newsurvey", "No course selected")
            return self.surveyinfo()


        # if survey already in system exit
        if(Survey.query.filter_by(course_id=courseID).first() != None):
            errorMSG("routes.newsurvey", "survey already exists!")
            return self.surveyinfo()	

        #date added here is the date the survey goes live
   
        # dateStart = datetime.now()
        # dateEnd = datetime.now()

        survey = Survey(survey_name, courseID)

        survey.date.date_start = startdate
        survey.date.date_end = enddate

        # add this survey to the course
        course.survey.append(survey)
        db_session.add(survey)


        current_user.survey.append(survey)

        db_session.commit()

        #note no users are added at this point

        return self.surveyinfo()
