import copy
from datetime import datetime
from flask import redirect, render_template, request, url_for
from server import errorMSG
from functions import get
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
					GeneralResponse, MCResponse
from models import Survey, Course, UniUser
from database import db_session
from flask_login import current_user


class SurveyUtil(object):
    def surveyinfo(self):
        if (current_user.is_authenticated) == False:
            return redirect(url_for("login"))

        # users only see the surveys/courses they are permitted to see!
        if(current_user.role == 'admin'):
            course_list = Course.query.all()
            survey_list = Survey.query.all()

        else:
            # course_list = current_user.courses
            survey_list = current_user.surveys
            course_list = current_user.courses

            # survey list needs to only hae surveys i can access at this time!

        return render_template("surveys.html", user=current_user,
                               course_list=course_list,
                               survey_list=survey_list)

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

        if current_user.role == 'student':

            # todo: check if student answered survey already here looking at survey.uniuser_id!
            if survey.status == 0:
                return self.surveyinfo()
            if survey.status == 1:
                return self.surveyinfo()
            if survey.status == 2:
                return render_template("answersurvey.html", survey=survey,
                                       course=course)
            if survey.status == 3:
                #open survey results
                return self.selfsurveyinfo()

        if current_user.role == 'admin' or current_user in survey.users:

            general = GeneralQuestion.query.all()
            multi = MCQuestion.query.all()

            surveygen = survey.gen_questions
            surveymc = survey.mc_questions

            return render_template("modifysurvey.html",user=current_user,surveygen=surveygen,surveymc=surveymc,survey=survey,course=course,general=general,multi=multi)

        return self.surveyinfo()

    def newsurvey(self):
        if (current_user.is_authenticated) == False:
            return redirect(url_for("login"))

        if(current_user.role != 'admin'):
            errorMSG("routes.newsurvey", "unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        survey_name = request.form["svyname"]
        courseID = request.form["svycourse"]

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

        # add this survey to the course
        course.survey.append(survey)
        db_session.add(survey)
        db_session.commit()

        #note no users are added at this point

        return self.surveyinfo()

    def addqsurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'admin' and current_user.role != 'staff'):
            errorMSG("routes.addqsurvey", "unauthorised user attempted access:",
                     current_user.id)
            return render_template("home.html", user=current_user)

        # get list of questions to add
        survey_questions = request.form.getlist('question')

        if survey_questions == []:
            errorMSG("routes.addqsurvey", "no questions selected")
            return self.opensurvey()

        if (request.form.getlist("surveyid") == []):
            errorMSG("routes.addqsurvey", "surveyid not selected")
            return self.surveyinfo()

        surveyID = request.form["surveyid"]

        survey = Survey.query.filter_by(id=surveyID).first()	
        if(survey == None):
            errorMSG("routes.addqsurvey", "survey object is empty")
            return self.surveyinfo()	

        # check this staff member is authorised to add to this survey
        # check that they are authorised to add the type of question

        # this sorts and stores the questions into the survey
        for question in survey_questions:
            if (question[1:2]=='0'):	
                question = MCQuestion.query.filter_by(id=int(question[4:5])).first()
                survey.mc_questions.append(question)
            elif (question[1:2]=='1'):
                question = GeneralQuestion.query.filter_by(id=int(question[4:5])).first()
                survey.gen_questions.append(question)

        db_session.commit()

        # reload page
        return self.opensurvey()

    def removeqsurvey(self):
        if (current_user.is_authenticated) == False:
            return redirect(url_for("login"))

        if(current_user.role != 'admin' and current_user.role != 'staff'):
            errorMSG("routes.removeqsurvey",
                     "unauthorised user attempted access:",
                     current_user.id)
            return render_template("home.html", user=current_user)

        if request.form.getlist('question')==[]:
            errorMSG("routes.removeqsurvey","no questions selected")
            return self.opensurvey()

        survey_question = request.form['question']

        if (request.form.getlist("surveyid")==[]):
            errorMSG("routes.removeqsurvey","surveyid not selected")
            return self.surveyinfo()

        surveyID = request.form["surveyid"]
        survey = Survey.query.filter_by(id=surveyID).first()	
        if(survey == None):
            errorMSG("routes.removeqsurvey","survey object is empty")
            return self.surveyinfo()	

        # remove question from the survey
        if (survey_question[1:2] == '0'):
            question = MCQuestion.query.filter_by(id=int(survey_question[4:5])).first()
            survey.mc_questions.remove(question)
        elif (survey_question[1:2]=='1'):
            question = GeneralQuestion.query.filter_by(id=int(survey_question[4:5])).first()
            survey.gen_questions.remove(question)

        db_session.commit()

        return self.opensurvey()

    def statussurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role == 'student'):
            errorMSG("routes.statussurvey","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        surveyID = request.form["surveyid"]

        survey = Survey.query.filter_by(id=surveyID).first()	
        if(survey==None):
            errorMSG("routes.statussurvey","survey object is empty")
            return self.surveyinfo()	

        # course = Course.query.filter_by(id=survey.course_id).first()	
        # if(course==None):
        #     errorMSG("routes.statussurvey","course object is empty")
        #     return self.surveyinfo()

        if survey.status == 0:
            if(current_user.role != 'admin'):
                errorMSG("routes.statussurvey","unauthorised user attempted access:",current_user.id)
                return render_template("home.html", user=current_user)
            survey.status = 1


            survey.add_staff()

            # staff = UniUser.query.filter_by(role='staff').all()	
            # if(staff==None):
            #     errorMSG("routes.statussurvey","staff object list is empty")
            #     return self.surveyinfo()

            # for s in staff:
            #     if(course in s.courses):
            #         survey.users.append(s)

        elif survey.status == 1:


            #note: according to specs she wants staff not to see the survey when its in 
            #"answer stage", but i have it they can see the survey just not do anything
            #and they cannot view results
            #reason for this is that staff wont know that there is a survey results coming soon
            #and they can now use past surveys they were associated with to maybe better choose
            #optional questions



            survey.status = 2

            survey.add_students()

            # students = UniUser.query.filter_by(role='student').all()	
            # if(students==None):
            #     errorMSG("routes.statussurvey","student object list is empty")
            #     return self.surveyinfo()

            # #give access to any students required
            # for s in students:
            #     if course in s.courses:
            #         survey.users.append(s)

        elif survey.status == 2:
            #anyone associated with the course will now have access to view its results
            survey.status = 3
        else:
            #cannot go past status 3 for a survey - view survey results status
            return self.viewsurvey()
        db_session.commit()

        return self.opensurvey()

    def viewsurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        print("view survey results now")

        #temp
        return self.opensurvey()

    def answersurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'student'):
            errorMSG("routes.answersurvey","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        #check student answered all fields
        surveyID = request.form["surveyid"]

        survey = Survey.query.filter_by(id=surveyID).first()	
        if(survey==None):
            errorMSG("routes.answersurvey","survey object is empty")
            return self.surveyinfo()	

        course = Course.query.filter_by(id=survey.course_id).first()	
        if(course==None):
            errorMSG("routes.answersurvey","course object is empty")
            return self.surveyinfo()

        genResponseList = []
        if len(survey.gen_questions)>0:

            genResponseList = request.form.getlist('genResponse')
            genResponseList = list(filter(None, genResponseList))

            if len(survey.gen_questions)!=len(genResponseList):
                errorMSG("routes.answersurvey","Extended Response Questions not completed")
                return self.opensurvey()

        for text in genResponseList:
            if (get.cleanString(str(text))==False):
                errorMSG("routes.answersurvey","Invalid input in extended response")
                return self.opensurvey()


        mcResponseList = []
        if len(survey.mc_questions)>0:
            for question in survey.mc_questions:
                if (request.form.getlist(str(question.id))==[]):
                    errorMSG("routes.answersurvey","MultiChoice Questions not completed")
                    return self.opensurvey()

                mcResponseList.append(request.form[str(question.id)])

        mcResponseList = list(filter(None, mcResponseList))

        if len(survey.mc_questions)!=len(mcResponseList):
            errorMSG("routes.answersurvey","MultiChoice Questions not completed")
            return self.opensurvey()


        #double check this person has not already responded? 

        surveyResponse = SurveyResponse(survey.id)
        db_session.add(surveyResponse)


        #this sorts and stores the answers into the survey response based on type
        for question,response in zip(survey.gen_questions,genResponseList):
            response = GeneralResponse(surveyResponse.id,question.id,response)
            surveyResponse.gen_responses.append(response)

        for question,response in zip(survey.mc_questions,mcResponseList):
            response = MCResponse(surveyResponse.id,question.id,response)
            surveyResponse.mc_responses.append(response)


        #remove the student from the survey list (so they cannont answer again)
        survey.users.remove(current_user)

        #commit the new survey response to this survey
        db_session.commit()

        #TODO: set survey to completed by this student to prevent resubmission!

        return redirect(url_for("submit"))

class QuestionUtil(object):
    def questioninfo(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'admin'):
            errorMSG("routes.questioninfo","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        #read in list of questions from db, filter out any not available to user or deleted
        general = GeneralQuestion.query.all()
        multi = MCQuestion.query.all()
        return render_template("questions.html",user=current_user,multi=multi,general=general)


    def openquestion(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'admin'):
            errorMSG("routes.openquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        if (request.form.getlist('question')==[]):
            errorMSG("routes.openquestion","question not selected")
            return self.questioninfo()		

        qID = request.form['question']
        questionType = 1

        #load up the question from db
        if (qID[1:2]=='0'):	
            questionObject = MCQuestion.query.filter_by(id=int(qID[4:5])).first()
        elif (qID[1:2]=='1'):
            questionObject = GeneralQuestion.query.filter_by(id=int(qID[4:5])).first()
            questionType = 2 #so we know if question type was modified in form
        if (questionObject==None):
            errorMSG("routes.openquestion","This question does not exist")
            return self.questioninfo()

        return render_template("modifyquestion.html",user=current_user,questionObject=questionObject,questionType=questionType)


    def addquestion(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'admin'):
            errorMSG("routes.addquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        question = request.form["question"]
        status = 0

        #by default a question is mandatory unless optional is checked
        if(request.form.getlist("optional")!=[]):
            status = 1

        if(question==""):
            errorMSG("append.question","No Question Provided")
            return self.questioninfo()

        for text in question:
            if (get.cleanString(str(text))==False):
                errorMSG("routes.createsurvey","Invalid input in fields")
                return self.questioninfo()


        if(request.form["qtype"]=='0'):
            new = GeneralQuestion(question,status)
            db_session.add(new)
            db_session.commit()
            return self.questioninfo()

        #multiple choice question
        answer_one = request.form["option_one"]
        answer_two = request.form["option_two"]
        answer_three = request.form["option_three"]
        answer_four = request.form["option_four"]

        #check for invalid characters
        answers = [answer_one,answer_two,answer_three,answer_four]
        answers = list(filter(None, answers))
        validStrings = copy.copy(answers)
        validStrings.append(question)

        for text in validStrings:
            if (get.cleanString(str(text))==False):
                errorMSG("routes.createsurvey","Invalid input in fields")
                return self.questioninfo()


        #if only one answer provided then return with error msg (this is not a valid question)
        if(len(answers)<2):
            errorMSG("routes.createsurvey","Only one answer provided for a mc question")
            return self.questioninfo()

        new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
        db_session.add(new)
        db_session.commit()

        return self.questioninfo()


    def modifyquestion(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'admin'):
            errorMSG("routes.modifyquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        oldType = request.form["oldType"] #old question type (was it MC or general?)
        qID = request.form["qID"]
        question = request.form["questiontitle"]

        status = 0

        if(request.form.getlist("optional")!=[]):
            status = 1

        #is the question getting deleted?
        if(request.form["delete"]=='1'):
            status = 2
        else:
            if(question==""):
                errorMSG("append.question","No Question Provided")
                return self.questioninfo()

            for text in question:
                if (get.cleanString(str(text))==False):
                    errorMSG("routes.modifyquestion","Invalid input in fields")
                    return self.openquestion()

        #open the correct question objecttype
        # 1 is MC, 2 is General
        if(oldType=='2'):
            qObject=GeneralQuestion.query.filter_by(id=qID).first()
        else:
            qObject=MCQuestion.query.filter_by(id=qID).first()	

        if(qObject==None):
            errorMSG("routes.modifyquestion ","No question object Found")
            return self.questioninfo()

        #is the question just getting deleted?
        if(status==2):
            qObject.status = status
            db_session.commit()
            return self.questioninfo()


        #extended response questions
        if(request.form["qtype"]=='0'):
            if(oldType=='2'):
                #same general type of question, just changing fields
                qObject.question = question
                qObject.status = status

            else:
                #change of question type - delete old type, and make new type
                qObject.status = 2
                new = GeneralQuestion(question,status)
                db_session.add(new)
                
            db_session.commit()	

            return self.questioninfo()	


        #only multiple choice questions will get past here!

        answer_one = request.form["option_one"]
        answer_two = request.form["option_two"]
        answer_three = request.form["option_three"]
        answer_four = request.form["option_four"]

        #check for invalid characters
        answers = [answer_one,answer_two,answer_three,answer_four]
        answers = list(filter(None, answers))
        validStrings = copy.copy(answers)
        validStrings.append(question)


        for text in validStrings:
            if (get.cleanString(str(text))==False):
                errorMSG("routes.createsurvey","Invalid input in fields")
                return self.openquestion()


        #if only one answer provided then return with error msg (this is not a valid question)
        if(len(answers)<2):
            errorMSG("routes.createsurvey","Only one answer provided for a mc question")
            return self.openquestion()

        #has by data type changed? If no, then I just update the MC fields
        if(oldType=='1'):
            qObject.question = question
            qObject.status = status
            qObject.answerOne = answer_one
            qObject.answerTwo = answer_two
            qObject.answerThree = answer_three
            qObject.answerFour = answer_four	
        else:
            #new mc question, set old question to deleted, and make new general question type
            qObject.status = 2
            new = MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
            db_session.add(new)
        
        db_session.commit()

        return self.questioninfo()