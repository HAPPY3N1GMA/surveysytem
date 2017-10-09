# def surveyinfo():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	#users only see the surveys/courses they are permitted to see!
# 	if(current_user.role == 'admin'):
# 		course_list = Course.query.all()
# 		survey_list = Survey.query.all()

# 	else:
# 		#course_list = current_user.courses
# 		survey_list = current_user.surveys
# 		course_list = current_user.courses


# 		#survey list needs to only hae surveys i can access at this time!

# 	return render_template("surveys.html",user=current_user,course_list=course_list,survey_list=survey_list)

# def opensurvey():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if (request.form.getlist("surveyid")==[]):
# 		errorMSG("routes.opensurvey","surveyid not selected")
# 		return surveyinfo()
	
# 	surveyID = request.form["surveyid"]

# 	survey = Survey.query.filter_by(id=surveyID).first()	
# 	if(survey==None):
# 		errorMSG("routes.opensurvey","survey object is empty")
# 		return surveyinfo()	

# 	course = Course.query.filter_by(id=survey.course_id).first()	
# 	if(course==None):
# 		errorMSG("routes.opensurvey","course object is empty")
# 		return surveyinfo()


# 	if current_user.role == 'student':

# 		#TODO: check if student answered survey already here looking at survey.uniuser_id!
# 		if survey.status==0:
# 			return surveyinfo()
# 		if survey.status==1:
# 			return surveyinfo()
# 		if survey.status==2:
# 			return render_template("answersurvey.html",survey=survey,course=course)
# 		if survey.status==3:
# 			#open survey results
# 			return surveyinfo()

# 	if current_user.role=='admin' or current_user in survey.users:

# 		general = GeneralQuestion.query.all()
# 		multi = MCQuestion.query.all()

# 		surveygen = survey.gen_questions
# 		surveymc = survey.mc_questions

# 		return render_template("modifysurvey.html",user=current_user,surveygen=surveygen,surveymc=surveymc,survey=survey,course=course,general=general,multi=multi)


# 	return surveyinfo()


# def newsurvey():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role != 'admin'):
# 		errorMSG("routes.newsurvey","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	survey_name = request.form["svyname"]
# 	courseID = request.form["svycourse"]


# 	print("NEW COURSE ID:",courseID)


# 	course = Course.query.filter_by(id=courseID).first()	
# 	if(course==None):
# 		errorMSG("routes.newsurvey","course object is empty")
# 		return surveyinfo()

# 	#qObject=Course.query.filter_by(id=courseID).first()

# 	if (get.cleanString(str(survey_name))==False):
# 		errorMSG("routes.newsurvey","Invalid Characters in survey name")
# 		return surveyinfo()

# 	if (str(courseID) == ''):
# 		errorMSG("routes.newsurvey","No course selected")
# 		return surveyinfo()


# 	#if survey already in system exit
# 	if(Survey.query.filter_by(course_id=courseID).first()!=None):
# 		errorMSG("routes.newsurvey","survey already exists!")
# 		return surveyinfo()	

# 	survey = Survey(survey_name,datetime.now(),courseID)

# 	#add this survey to the course
# 	course.survey.append(survey)
# 	staff_affected = course.uniusers
# 	# print(staff_affected)
# 	db_session.add(survey)
# 	db_session.commit()

# 	for user in staff_affected:
# 		user.surveys.append(survey)

# 	db_session.commit()

# 	return surveyinfo()


# def addqsurvey():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))


# 	if(current_user.role != 'admin' and current_user.role != 'staff'):
# 		errorMSG("routes.addqsurvey","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	#get list of questions to add
# 	survey_questions = request.form.getlist('question')

# 	if survey_questions==[]:
# 		errorMSG("routes.addqsurvey","no questions selected")
# 		return opensurvey()


# 	if (request.form.getlist("surveyid")==[]):
# 		errorMSG("routes.addqsurvey","surveyid not selected")
# 		return surveyinfo()
	
# 	surveyID = request.form["surveyid"]

# 	survey = Survey.query.filter_by(id=surveyID).first()	
# 	if(survey==None):
# 		errorMSG("routes.addqsurvey","survey object is empty")
# 		return surveyinfo()	



# 	#check this staff member is authorised to add to this survey
# 	#check that they are authorised to add the type of question



# 	#this sorts and stores the questions into the survey
# 	for question in survey_questions:
# 		if (question[1:2]=='0'):	
# 			question = MCQuestion.query.filter_by(id=int(question[4:5])).first()
# 			survey.mc_questions.append(question)
# 		elif (question[1:2]=='1'):
# 			question = GeneralQuestion.query.filter_by(id=int(question[4:5])).first()
# 			survey.gen_questions.append(question)

# 	db_session.commit()

# 	#reload page
# 	return opensurvey()

# def removeqsurvey():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role != 'admin' and current_user.role != 'staff'):
# 		errorMSG("routes.removeqsurvey","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)
	
# 	if request.form.getlist('question')==[]:
# 		errorMSG("routes.removeqsurvey","no questions selected")
# 		return opensurvey()

# 	survey_question = request.form['question']

# 	if (request.form.getlist("surveyid")==[]):
# 		errorMSG("routes.removeqsurvey","surveyid not selected")
# 		return surveyinfo()
	
# 	surveyID = request.form["surveyid"]
# 	survey = Survey.query.filter_by(id=surveyID).first()	
# 	if(survey==None):
# 		errorMSG("routes.removeqsurvey","survey object is empty")
# 		return surveyinfo()	

# 	#remove question from the survey
# 	if (survey_question[1:2]=='0'):	
# 		question = MCQuestion.query.filter_by(id=int(survey_question[4:5])).first()
# 		survey.mc_questions.remove(question)
# 	elif (survey_question[1:2]=='1'):
# 		question = GeneralQuestion.query.filter_by(id=int(survey_question[4:5])).first()
# 		survey.gen_questions.remove(question)

# 	db_session.commit()

# 	return opensurvey()

# def statussurvey():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role == 'student'):
# 		errorMSG("routes.statussurvey","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	surveyID = request.form["surveyid"]

# 	survey = Survey.query.filter_by(id=surveyID).first()	
# 	if(survey==None):
# 		errorMSG("routes.statussurvey","survey object is empty")
# 		return surveyinfo()	

# 	course = Course.query.filter_by(id=survey.course_id).first()	
# 	if(course==None):
# 		errorMSG("routes.statussurvey","course object is empty")
# 		return surveyinfo()

# 	if survey.status == 0:
# 		if(current_user.role != 'admin'):
# 			errorMSG("routes.statussurvey","unauthorised user attempted access:",current_user.id)
# 			return render_template("home.html", user=current_user)
# 		survey.status = 1

# 		staff = UniUser.query.filter_by(role='staff').all()	
# 		if(staff==None):
# 			errorMSG("routes.statussurvey","staff object list is empty")
# 			return surveyinfo()

# 		for s in staff:
# 			if(course in s.courses):
# 				survey.users.append(s)

# 	elif survey.status == 1:


# 		#NOTE: according to specs she wants staff not to see the survey when its in 
# 		#"answer stage", but i have it they can see the survey just not do anything
# 		#and they cannot view results
# 		#reason for this is that staff wont know that there is a survey results coming soon
# 		#and they can now use past surveys they were associated with to maybe better choose
# 		#optional questions



# 		survey.status = 2
# 		students = UniUser.query.filter_by(role='student').all()	
# 		if(students==None):
# 			errorMSG("routes.statussurvey","student object list is empty")
# 			return surveyinfo()

# 		#give access to any students required
# 		for s in students:
# 			if course in s.courses:
# 				survey.users.append(s)

# 	elif survey.status == 2:
# 		#anyone associated with the course will now have access to view its results
# 		survey.status = 3
# 	else:
# 		#cannot go past status 3 for a survey - view survey results status
# 		return viewsurvey()
# 	db_session.commit()

# 	return opensurvey()

# def viewsurvey():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	print("view survey results now")

# 	#temp
# 	return opensurvey()


# def answersurvey():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role != 'student'):
# 		errorMSG("routes.answersurvey","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	#check student answered all fields
# 	surveyID = request.form["surveyid"]

# 	survey = Survey.query.filter_by(id=surveyID).first()	
# 	if(survey==None):
# 		errorMSG("routes.answersurvey","survey object is empty")
# 		return surveyinfo()	

# 	course = Course.query.filter_by(id=survey.course_id).first()	
# 	if(course==None):
# 		errorMSG("routes.answersurvey","course object is empty")
# 		return surveyinfo()

# 	genResponseList = []
# 	if len(survey.gen_questions)>0:

# 		genResponseList = request.form.getlist('genResponse')
# 		genResponseList = list(filter(None, genResponseList))

# 		if len(survey.gen_questions)!=len(genResponseList):
# 			errorMSG("routes.answersurvey","Extended Response Questions not completed")
# 			return opensurvey()

# 	for text in genResponseList:
# 		if (get.cleanString(str(text))==False):
# 			errorMSG("routes.answersurvey","Invalid input in extended response")
# 			return opensurvey()


# 	mcResponseList = []
# 	if len(survey.mc_questions)>0:
# 		for question in survey.mc_questions:
# 			if (request.form.getlist(str(question.id))==[]):
# 				errorMSG("routes.answersurvey","MultiChoice Questions not completed")
# 				return opensurvey()

# 			mcResponseList.append(request.form[str(question.id)])

# 	mcResponseList = list(filter(None, mcResponseList))

# 	if len(survey.mc_questions)!=len(mcResponseList):
# 		errorMSG("routes.answersurvey","MultiChoice Questions not completed")
# 		return opensurvey()


# 	#double check this person has not already responded? 

# 	surveyResponse = SurveyResponse(survey.id)
# 	db_session.add(surveyResponse)


# 	#this sorts and stores the answers into the survey response based on type
# 	for question,response in zip(survey.gen_questions,genResponseList):
# 		response = GeneralResponse(surveyResponse.id,question.id,response)
# 		surveyResponse.gen_responses.append(response)

# 	for question,response in zip(survey.mc_questions,mcResponseList):
# 		response = MCResponse(surveyResponse.id,question.id,response)
# 		surveyResponse.mc_responses.append(response)


# 	#remove the student from the survey list (so they cannont answer again)
# 	survey.users.remove(current_user)

# 	#commit the new survey response to this survey
# 	db_session.commit()




# 	#TODO: set survey to completed by this student to prevent resubmission!



# 	return redirect(url_for("submit"))