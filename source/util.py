import copy
from datetime import datetime
from flask import redirect, render_template, request, url_for, flash
from functions import get
# from models import questions_model.GeneralQuestion, questions_model.MCQuestion, surveys_model.SurveyResponse,\
# 					questions_model.GeneralResponse, questions_model.MCResponse
#from models import surveys_model.Survey, courses_model.Course, users_model.UniUser

from models import users_model, surveys_model, questions_model, courses_model

from database import db_session
from flask_login import current_user
from classes import survey_usage, common, course_usage

class SurveyUtil(object):


    def surveyinfo(self):
        return render_template("surveys.html",user=current_user)




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




    def viewsurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        print("view survey results now")

        #temp
        return survey_usage.OpenSurvey().open_attempt()	



    def answersurvey(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

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

class QuestionUtil(object):
    def questioninfo(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.questioninfo","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        #read in list of questions from db, filter out any not available to user or deleted
        general = questions_model.GeneralQuestion.query.all()
        multi = questions_model.MCQuestion.query.all()
        return render_template("questions.html",user=current_user,multi=multi,general=general)


    def openquestion(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.openquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        if (request.form.getlist('question')==[]):
            flash('No question selected')
            common.Debug.errorMSG("routes.openquestion","question not selected")
            return self.questioninfo()		

        qID = request.form['question']
        questionType = 1

        #load up the question from db
        if (qID[1:2]=='0'):	
            questionObject = questions_model.MCQuestion.query.filter_by(id=int(qID[4:5])).first()
        elif (qID[1:2]=='1'):
            questionObject = questions_model.GeneralQuestion.query.filter_by(id=int(qID[4:5])).first()
            questionType = 2 #so we know if question type was modified in form
        if (questionObject==None):
            common.Debug.errorMSG("routes.openquestion","This question does not exist")
            return self.questioninfo()

        return render_template("modifyquestion.html",user=current_user,questionObject=questionObject,questionType=questionType)


    def addquestion(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.addquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        question = request.form["question"]
        status = 0

        #by default a question is mandatory unless optional is checked
        if(request.form.getlist("optional")!=[]):
            status = 1

        if(question==""):
            common.Debug.errorMSG("append.question","No Question Provided")
            flash('Please Enter A Valid Question')
            return self.questioninfo()

        for text in question:
            if (get.cleanString(str(text))==False):
                common.Debug.errorMSG("routes.createsurvey","Invalid input in fields")
                flash('Invalid characters in question')
                return self.questioninfo()


        if(request.form["qtype"]=='0'):
            new = questions_model.GeneralQuestion(question,status)
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
                common.Debug.errorMSG("routes.createsurvey","Invalid input in fields")
                flash('Invalid characters in answers')
                return self.questioninfo()


        #if only one answer provided then return with error msg (this is not a valid question)
        if(len(answers)<2):
            common.Debug.errorMSG("routes.createsurvey","Only one answer provided for a mc question")
            flash("Multiple choice questions require atleast 2 answers")
            return self.questioninfo()

        new = questions_model.MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
        db_session.add(new)
        db_session.commit()

        return self.questioninfo()


    def modifyquestion(self):
        if (current_user.is_authenticated)==False:
            return redirect(url_for("login"))

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.modifyquestion","unauthorised user attempted access:",current_user.id)
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
                common.Debug.errorMSG("append.question","No Question Provided")
                flash('Please Enter A Valid Question')
                return self.questioninfo()

            for text in question:
                if (get.cleanString(str(text))==False):
                    common.Debug.errorMSG("routes.modifyquestion","Invalid input in fields")
                    flash('Invalid characters in question')
                    return self.openquestion()

        #open the correct question objecttype
        # 1 is MC, 2 is General
        if(oldType=='2'):
            qObject=questions_model.GeneralQuestion.query.filter_by(id=qID).first()
        else:
            qObject=questions_model.MCQuestion.query.filter_by(id=qID).first()	

        if(qObject==None):
            common.Debug.errorMSG("routes.modifyquestion ","No question object Found")
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
                new = questions_model.GeneralQuestion(question,status)
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
                common.Debug.errorMSG("routes.createsurvey","Invalid input in fields")
                flash('Invalid characters in answers')
                return self.openquestion()


        #if only one answer provided then return with error msg (this is not a valid question)
        if(len(answers)<2):
            common.Debug.errorMSG("routes.createsurvey","Multiple choice questions require atleast 2 answers")
            flash("Multiple choice questions require atleast 2 answers")
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
            new = questions_model.MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
            db_session.add(new)
        
        db_session.commit()

        return self.questioninfo()