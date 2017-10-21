#creating/modifying questions in here


import ast, os, time, copy
from datetime import datetime
from flask import Flask, request, flash
from functions import get

#from models import Survey, Course, UniUser, Admin, Staff, Student, Guest
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
				print(question.question)
			elif (questioninfo[0]==1):
				question = questions_model.GeneralQuestion.query.filter_by(id=int(questioninfo[1])).first()
				print(question.question)
		return question

