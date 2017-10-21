import ast, os, time, copy
from datetime import datetime
from flask import Flask, request, flash
from functions import get
from models import surveys_model, courses_model, questions_model
from flask_login import current_user
from abc import ABCMeta, abstractmethod
from classes import course_usage, common, survey_usage


class QuestionType:
    def type(questioninfo = []):
        question = None
        if questioninfo:
            if (questioninfo[0] == 0):
                question = questions_model.MCQuestion.query.filter_by(id=int(questioninfo[1])).first()
            elif (questioninfo[0]==1):
                question = questions_model.GeneralQuestion.query.filter_by(id=int(questioninfo[1])).first()
        return question


class OpenQuestion:
    def open_attempt(self):
        'opens a specific question for modification'
        question = request.form.getlist('question')
        if question:
            question = ast.literal_eval(question[0])
            question = QuestionType.type(question)
            if question:
                if question.status == 2:
                    flash("That Question has already been Deleted")
                    return common.Render.questions()
                return current_user.OpenQuestion(question)
        else:
            flash("Please Select a Question to Open")
        return common.Render.questions()


class CreateQuestion:
    'creates a new question'
    def create_attempt(self):
        question = request.form["question"]
        status = 0
        newquestion = None
        if question != "":
            if request.form.getlist("optional"):
                status = 1
            clean = True
            for text in question:
                if get.cleanString(str(text)) == False:
                    clean = False
                    flash('Invalid characters in question')
            if clean:
                if request.form["qtype"]=='1':
                    answer_one = request.form["option_one"]
                    answer_two = request.form["option_two"]
                    answer_three = request.form["option_three"]
                    answer_four = request.form["option_four"]

                    answers = [answer_one,answer_two,answer_three,answer_four]
                    answers = list(filter(None, answers))
                    validStrings = copy.copy(answers)
                    validStrings.append(question)

                    for text in validStrings:
                        if get.cleanString(str(text))==False:
                            clean = False
                            flash('Invalid characters in answers')  
                    if clean:
                        if len(answers) > 1:
                            newquestion = questions_model.MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
                            return current_user.createQuestion(newquestion)
                        else:
                            flash("Multiple choice questions require atleast 2 answers")
                else:
                    newquestion = questions_model.GeneralQuestion(question,status)
                    return current_user.createQuestion(newquestion)
                              
        else:
            flash('Please Enter A Valid Question')

        return current_user.ViewAllQuestions()


class ModifyQuestion:
    'Modifys a question'
    def modify_attempt(self):
        oldType = request.form["oldType"]
        qID = request.form["qID"]
        question = request.form["questiontitle"]
        status = 0

        if request.form.getlist("optional"):
            status = 1
        if(oldType=='2'):
            qObject=questions_model.GeneralQuestion.query.filter_by(id=qID).first()
        else:
            qObject=questions_model.MCQuestion.query.filter_by(id=qID).first()  

        if qObject is None:
            return common.Render.questions()

        if qObject.status == 2:
            flash("That Question has already been Deleted")
            return common.Render.questions()

        if request.form["delete"] == '1':
            status = 2
        else:
            if question != "":
                for text in question:
                    if get.cleanString(str(text)) == False:
                        flash('Invalid characters in question')
                        return current_user.OpenQuestion(qObject)
            else:
                flash('Please Enter A Valid Question')
                return current_user.OpenQuestion(qObject)

        # 1 is MC, 2 is General
        if(status==2):
            return current_user.deleteQuestion(qObject)

        if(request.form["qtype"]=='0'):
            return current_user.updateGenQuestion(qObject,oldType,question,status)


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
                flash('Invalid characters in answers')
                return current_user.OpenQuestion(qObject)

        #if only one answer provided then return with error msg (this is not a valid question)
        if(len(answers)<2):
            flash("Multiple choice questions require atleast 2 answers")
            return current_user.OpenQuestion(qObject)


        return current_user.updateMCQuestion(qObject,oldType,question,status,answer_one,
                                             answer_two,answer_three,answer_four)





