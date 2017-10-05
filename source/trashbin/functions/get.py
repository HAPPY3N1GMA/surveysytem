import csv, ast, os, re
from classes import fileclasses
from functions import append
from server import errorMSG


#build list of survey questions
def questionList(sID):
	survey = fileclasses.survey.sID(str(sID))
	questionList = []
	if survey is not None:
		#using qID's, create list of questions from master
		for qID in survey.questionList:
			question = fileclasses.question.qID(qID)
			if question is not None:	
				#clean up formatting of list
				questionList = questionList+[[qID,question.questionName,question.answers]]
				questionList = str(questionList).replace('"',"")			
				questionList = ast.literal_eval(str(questionList))
			else:
				errorMSG("questionList","No questions found!")
	return questionList

#checks for invalid characters in string
#return True if clean, false if not
def cleanString(inputString):
	invalid = re.compile(r"[/[\]{}~`<>]");
	if invalid.search(inputString):
	    return False
	else:
	    return True