import csv, ast, os
from classes import fileclasses
from functions import append
from server import errorMSG



#build list of survey questions

def questionList(sID):
	mastercsv = fileclasses.csvfile("master_survey.csv")
	surveyInfo = mastercsv.readfromid(sID)

	questionList = []

	if surveyInfo is not None:
		#grab list of question Id's
		questionIDs = ast.literal_eval(surveyInfo[4])
		questioncsv = fileclasses.csvfile("master_question.csv")

		#using qID's, create list of questions from master
		for qID in questionIDs:	
			questionList = questionList+[(questioncsv.readfromid(qID))]

	return questionList