import ast, os, time, copy
from datetime import datetime
from flask import Flask, request, flash, render_template
from functions import get

#from models import Survey, Course, UniUser, Admin, Staff, Student, Guest
from models import surveys_model, courses_model


from flask_login import login_user, login_required, current_user, logout_user
from abc import ABCMeta, abstractmethod
from classes import course_usage, question_usage, common


class CreateSurvey:
    'creates a new survey'
    def create_attempt(self):
        courseId = request.form["svycourse"]
        surveyName = request.form["svyname"]
        startDate = request.form["startdate"]
        endDate = request.form["enddate"]

        if CreateSurvey.err_check(courseId,surveyName,startDate,endDate):
            startDate = datetime.strptime(startDate, '%Y/%m/%d')
            endDate = datetime.strptime(endDate, '%Y/%m/%d')
            return current_user.CreateSurvey(courseId,surveyName,startDate,endDate)

        return common.Render.surveys()


    def err_check(courseId='',surveyName='',startDate='',endDate=''):
        'checks a new surveys form fields'
        if surveyName == '':
            flash('Please Enter a Valid Survey Name')
            return False

        if (get.cleanString(str(surveyName)) == False):
            errorMSG("routes.newsurvey", "Invalid Characters in survey name")
            return False

        try:
            startDate = datetime.strptime(startDate, '%Y/%m/%d')
            endDate = datetime.strptime(endDate, '%Y/%m/%d')
        except ValueError:
            flash('Please Enter a Start and Finish Date')
            return False
        
        if endDate <= startDate:
            flash('Invalid Start/End Date')
            return False

        if endDate <= datetime.today():
            flash('Invalid End Date')
            return False

        course = courses_model.Course.query.filter_by(id=courseId).first()    
        if(course == None):
            errorMSG("routes.newsurvey", "course object is empty")
            return False

        if LoadSurvey.load(request.form.getlist('surveyid')):
            errorMSG("routes.newsurvey", "survey already exists!")
            return False

        return True


class OpenSurvey:
    'opens a specific survey to required page'
    def open_attempt(self):

        survey = LoadSurvey.load(request.form.getlist('surveyid'))
        if survey:
            course = course_usage.LoadCourse.load(survey.course_id)  
            if course:
                if survey.status == 3:
                    return current_user.OpenPublishedSurvey(survey, course)
                else:
                    return current_user.ModifySurvey(survey, course)
        else:
            flash("Please Select a Survey to Open")
        return common.Render.surveys()



class LoadSurvey:
    'loads a specific survey'
    def load(surveyID=[]):
        if surveyID:
            survey = surveys_model.Survey.query.filter_by(id=surveyID[0]).first()    
            return survey
        return None



class StatusSurvey:
    'updates the status of the survey'
    def update_attempt(self):
        survey = LoadSurvey.load(request.form.getlist('surveyid'))
        course = course_usage.LoadCourse.load(survey.course_id)  
        
        if survey and course: 
            if survey.status == 0:
                return current_user.PushSurvey(survey,course)
            if survey.status == 1:    
                return current_user.PublishSurvey(survey,course)
            if survey.status == 3:
                return current_user.EndSurvey(survey,course)
            if survey.status == 4:
                return current_user.ViewSurveyResultsRequest(survey.id) 

        return OpenSurvey().open_attempt() 



class AddQuestionSurvey:
    'adds questions to surveys'
    def add_attempt(self):

        add_status = AddFailure()
        survey = None
        course = None
        questions = []
        survey_questions = request.form.getlist('question')
        if survey_questions:
            survey = LoadSurvey.load(request.form.getlist('surveyid'))
            if survey:
                course = course_usage.LoadCourse.load(survey.course_id)  
                if course:
                    for q in survey_questions:
                        q = ast.literal_eval(q)
                        q = question_usage.QuestionType.type(q)
                        if q:
                            questions.append(q)
                    if questions:
                        add_status = AddSuccess()
        else:
            flash('No questions selected')

        return add_status.execute(questions,survey,course)  

class AddStatus:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self,survey_questions=[],survey=None,course=None):
        pass

class AddSuccess(AddStatus):
    'purpose: handles a good add question request'

    def execute(self,survey_questions=[],survey=None,course=None):
        return current_user.AddQuestionSurvey(survey_questions,survey,course)

class AddFailure(AddStatus):
    'purpose: handles a bad add question request'

    def execute(self,survey_questions=[],survey=None,course=None):
        return OpenSurvey().open_attempt()   



class RemoveQuestionSurvey:
    'removes a question from a survey'
    def remove_attempt(self):

        remove_status = RemoveFailure()
        survey_question = request.form.getlist('question')
        survey = None
        course = None
        question = None
        if survey_question:
            survey_question = request.form['question']
            survey = LoadSurvey.load(request.form.getlist('surveyid'))
            if survey:
                course = course_usage.LoadCourse.load(survey.course_id)  
                if course:
                    survey_question = ast.literal_eval(survey_question)
                    question = question_usage.QuestionType.type(survey_question)
                    if question:
                        remove_status = RemoveSuccess()
        else:
            flash('No question selected')

        return remove_status.execute(question,survey,course)    
        #return OpenSurvey().open_attempt()         


class RemoveStatus:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self,question=None,survey=None,course=None):
        pass

class RemoveSuccess(RemoveStatus):
    'purpose: handles a good remove question request'

    def execute(self,question=None,survey=None,course=None):
        return current_user.RemoveQuestionSurvey(question,survey,course)

class RemoveFailure(RemoveStatus):
    'purpose: handles a bad remove question request'

    def execute(self,question=None,survey=None,course=None):
        return OpenSurvey().open_attempt()   


class AnswerSurvey:

    def answer_attempt(self):

        survey = LoadSurvey.load(request.form.getlist('surveyid'))
        if survey:
            course = course_usage.LoadCourse.load(survey.course_id)  
            if course:
                if current_user in survey.users:
                    genResponseList = self.getGenResponse(survey)
                    if genResponseList is not None:
                        mcResponseList = self.getMCResponse(survey)
                        if mcResponseList is not None:
                            return current_user.AnswerSurvey(survey,mcResponseList,genResponseList)

        return OpenSurvey().open_attempt()   



    def getGenResponse(self,survey=None):
        genResponseList = []
        if len(survey.gen_questions)>0:
            genResponseList = request.form.getlist('genResponse')
            genResponseList = list(filter(None, genResponseList))

            if len(survey.gen_questions)!=len(genResponseList):
                flash('Please Complete All Extended Response Questions')
                return None

            for text in genResponseList:
                if (get.cleanString(str(text))==False):
                    flash('Invalid Characters Used In Extended Response')
                    return None

        return genResponseList


    def getMCResponse(self,survey=None):
        mcResponseList = []
        if len(survey.mc_questions)>0:
            for question in survey.mc_questions:
                if (request.form.getlist(str(question.id))==[]):
                    flash('Please Complete All Multiple Choice Questions')
                    return None

                mcResponseList.append(request.form[str(question.id)])

        mcResponseList = list(filter(None, mcResponseList))

        if len(survey.mc_questions)!=len(mcResponseList):
            flash('Please Complete All Multiple Choice Questions')
            return None

        return mcResponseList




class ViewSurveyResults:

    def view_attempt(self,survey):

        num_responses = len(survey.responses)
        mcdata = []

        if num_responses == 0:
            flash('There are no results at this time')
            return OpenSurvey().open_attempt()  

        #build the data for the mc pie charts
        for question in survey.mc_questions:
            mc_responses = []
            for response in survey.responses:
                for mc_response in response.mc_responses:
                    if mc_response.question_id == question.id:
                        mc_responses.append(mc_response)

            list_of_lists = []

            colours = []
            labels = []
            data = []  # the above list in percentages
            a_one = 0
            a_two = 0
            a_th = 0
            a_four = 0
            for resp in mc_responses:
                if resp.response == '1':
                  a_one += 1
                if resp.response == '2':
                  a_two += 1
                if resp.response == '3':
                  a_th += 1
                if resp.response == '4':
                  a_four += 1

            
            dataone = [a_one/num_responses,question.answerOne]
            datatwo = [a_two/num_responses,question.answerTwo]
            datathree = [a_th/num_responses,question.answerThree]
            datafour = [a_four/num_responses,question.answerFour]

            mcdata.append([question,[dataone,datatwo,datathree,datafour],num_responses])

            colours.append("red")
            colours.append("green")
            colours.append("blue")
            colours.append("yellow")

        return render_template("results.html", survey=survey,mcdata=mcdata)

#######################################################################
##########################      LOGIN    ##############################
#######################################################################

