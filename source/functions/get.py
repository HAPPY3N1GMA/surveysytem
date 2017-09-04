import csv, ast, os
from classes import fileclasses
from functions import append
from server import errorMSG




#build list of survey questions

def questionList(sID):
	survey = fileclasses.survey.read(str(sID))
	questionList = []

	print("survey:",survey)

	if survey is not None:
		#grab list of question Id's
		#questioncsv = fileclasses.csvfile("master_question.csv")

		#using qID's, create list of questions from master
		for qID in survey.questionList:

			#questionList = questionList+[(questioncsv.readfromid(qID))]

			question = fileclasses.question.read(qID)
			if question is not None:	
				#clean up formatting of list
				questionList = questionList+[[qID,question.questionName,question.answers]]
				questionList = str(questionList).replace('"',"")			
				questionList = ast.literal_eval(str(questionList))
	return questionList