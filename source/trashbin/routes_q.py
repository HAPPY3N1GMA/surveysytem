# def questioninfo():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role != 'admin'):
# 		errorMSG("routes.questioninfo","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	#read in list of questions from db, filter out any not available to user or deleted
# 	general = GeneralQuestion.query.all()
# 	multi = MCQuestion.query.all()
# 	return render_template("questions.html",user=current_user,multi=multi,general=general)


# def openquestion():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role != 'admin'):
# 		errorMSG("routes.openquestion","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	if (request.form.getlist('question')==[]):
# 		errorMSG("routes.openquestion","question not selected")
# 		return questioninfo()		

# 	qID = request.form['question']
# 	questionType = 1

# 	#load up the question from db
# 	if (qID[1:2]=='0'):	
# 		questionObject = MCQuestion.query.filter_by(id=int(qID[4:5])).first()
# 	elif (qID[1:2]=='1'):
# 		questionObject = GeneralQuestion.query.filter_by(id=int(qID[4:5])).first()
# 		questionType = 2 #so we know if question type was modified in form
# 	if (questionObject==None):
# 		errorMSG("routes.openquestion","This question does not exist")
# 		return questioninfo()

# 	return render_template("modifyquestion.html",user=current_user,questionObject=questionObject,questionType=questionType)


# def addquestion():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role != 'admin'):
# 		errorMSG("routes.addquestion","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	question = request.form["question"]
# 	status = 0

# 	#by default a question is mandatory unless optional is checked
# 	if(request.form.getlist("optional")!=[]):
# 		status = 1

# 	if(question==""):
# 		errorMSG("append.question","No Question Provided")
# 		return questioninfo()

# 	for text in question:
# 		if (get.cleanString(str(text))==False):
# 			errorMSG("routes.createsurvey","Invalid input in fields")
# 			return questioninfo()


# 	if(request.form["qtype"]=='0'):
# 		new = GeneralQuestion(question,status)
# 		db_session.add(new)
# 		db_session.commit()
# 		return questioninfo()

# 	#multiple choice question
# 	answer_one = request.form["option_one"]
# 	answer_two = request.form["option_two"]
# 	answer_three = request.form["option_three"]
# 	answer_four = request.form["option_four"]

# 	#check for invalid characters
# 	answers = [answer_one,answer_two,answer_three,answer_four]
# 	answers = list(filter(None, answers))
# 	validStrings = copy.copy(answers)
# 	validStrings.append(question)

# 	for text in validStrings:
# 		if (get.cleanString(str(text))==False):
# 			errorMSG("routes.createsurvey","Invalid input in fields")
# 			return questioninfo()


# 	#if only one answer provided then return with error msg (this is not a valid question)
# 	if(len(answers)<2):
# 		errorMSG("routes.createsurvey","Only one answer provided for a mc question")
# 		return questioninfo()

# 	new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
# 	db_session.add(new)
# 	db_session.commit()

# 	return questioninfo()


# def modifyquestion():
# 	if (current_user.is_authenticated)==False:
# 		return redirect(url_for("login"))

# 	if(current_user.role != 'admin'):
# 		errorMSG("routes.modifyquestion","unauthorised user attempted access:",current_user.id)
# 		return render_template("home.html", user=current_user)

# 	oldType = request.form["oldType"] #old question type (was it MC or general?)
# 	qID = request.form["qID"]
# 	question = request.form["questiontitle"]

# 	status = 0

# 	if(request.form.getlist("optional")!=[]):
# 		status = 1

# 	#is the question getting deleted?
# 	if(request.form["delete"]=='1'):
# 		status = 2
# 	else:
# 		if(question==""):
# 			errorMSG("append.question","No Question Provided")
# 			return questioninfo()

# 		for text in question:
# 			if (get.cleanString(str(text))==False):
# 				errorMSG("routes.modifyquestion","Invalid input in fields")
# 				return openquestion()

# 	#open the correct question objecttype
# 	# 1 is MC, 2 is General
# 	if(oldType=='2'):
# 		qObject=GeneralQuestion.query.filter_by(id=qID).first()
# 	else:
# 		qObject=MCQuestion.query.filter_by(id=qID).first()	

# 	if(qObject==None):
# 		errorMSG("routes.modifyquestion ","No question object Found")
# 		return questioninfo()

# 	#is the question just getting deleted?
# 	if(status==2):
# 		qObject.status = status
# 		db_session.commit()
# 		return questioninfo()


# 	#extended response questions
# 	if(request.form["qtype"]=='0'):
# 		if(oldType=='2'):
# 			#same general type of question, just changing fields
# 			qObject.question = question
# 			qObject.status = status

# 		else:
# 			#change of question type - delete old type, and make new type
# 			qObject.status = 2
# 			new = GeneralQuestion(question,status)
# 			db_session.add(new)
			
# 		db_session.commit()	

# 		return questioninfo()	


# 	#only multiple choice questions will get past here!

# 	answer_one = request.form["option_one"]
# 	answer_two = request.form["option_two"]
# 	answer_three = request.form["option_three"]
# 	answer_four = request.form["option_four"]

# 	#check for invalid characters
# 	answers = [answer_one,answer_two,answer_three,answer_four]
# 	answers = list(filter(None, answers))
# 	validStrings = copy.copy(answers)
# 	validStrings.append(question)


# 	for text in validStrings:
# 		if (get.cleanString(str(text))==False):
# 			errorMSG("routes.createsurvey","Invalid input in fields")
# 			return openquestion()


# 	#if only one answer provided then return with error msg (this is not a valid question)
# 	if(len(answers)<2):
# 		errorMSG("routes.createsurvey","Only one answer provided for a mc question")
# 		return openquestion()

# 	#has by data type changed? If no, then I just update the MC fields
# 	if(oldType=='1'):
# 		qObject.question = question
# 		qObject.status = status
# 		qObject.answerOne = answer_one
# 		qObject.answerTwo = answer_two
# 		qObject.answerThree = answer_three
# 		qObject.answerFour = answer_four	
# 	else:
# 		#new mc question, set old question to deleted, and make new general question type
# 		qObject.status = 2
# 		new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
# 		db_session.add(new)
	
# 	db_session.commit()

# 	return questioninfo()