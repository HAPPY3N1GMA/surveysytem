import csv, ast, os
from classes import fileclasses
from functions import append
from server import errorMSG




#build list of survey questions

def questionList(sID):
	survey = fileclasses.survey.read(str(sID))
	questionList = []
	if survey is not None:
		#using qID's, create list of questions from master
		for qID in survey.questionList:
			question = fileclasses.question.read(qID)
			if question is not None:	
				#clean up formatting of list
				questionList = questionList+[[qID,question.questionName,question.answers]]
				questionList = str(questionList).replace('"',"")			
				questionList = ast.literal_eval(str(questionList))
	return questionList