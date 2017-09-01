import csv, ast, os
from classes import fileclasses
from functions import append
from server import errorMSG



#####################################################################
# 					append.answer()									#
#																	#
# appends a new answer result to a question for a specified survey  #
#																	#
# 	Input: 															#
#			SurveyID 	- String									#														#														#
# 			QuestionID 	- String									#														#
# 			Answer 		- String									#
#																	#
# Sample CSV Format: 1,"['a', 'a', 'b', 'b', 'c', 'a', 'd', 'j']" 	#
#####################################################################

def answer(sID, qID, answer):

	if(sID==""):
		errorMSG("append.answer","No sID Provided")
		return
	if(qID==""):
		errorMSG("append.answer","No qID Provided")
		return
	if(answer==""):
		errorMSG("append.answer","No Answer Provided")
		return

	file = str(sID)+".csv"
	tmp = str(sID)+"_tmp.csv"	

	try:
		with open(file, 'r+') as csvReadFile:
			fieldnames = ['question_id', 'answers']
			reader = csv.DictReader(csvReadFile, fieldnames=fieldnames)
			with open (tmp, 'w') as write_row:
				writer=csv.DictWriter(write_row, fieldnames=fieldnames)
				for row in reader:
					if(row['question_id']==qID):
						tmp_list=ast.literal_eval(row['answers'])
						tmp_list.append(answer)
						row['answers'] = tmp_list
					writer.writerow(row)				
		os.remove(file)
		os.rename(tmp, file)
	except IOError:
		errorMSG("append.answer","No Survey Results File Found")
		return	

#####################################################
# 				append.question() 					#
#####################################################

def question(sID, question, answers): #assumes all params are strings

	if(sID==""):
		errorMSG("append.question","No sID Provided")
		return
	if(question==""):
		errorMSG("append.question","No Question Provided")
		return
	if(answers==""):
		errorMSG("append.question","No Answers Provided")
		return

	ID = fileclasses.textfile("questionID.txt")
	qID = ID.updateID()

	append.master_question(qID, question, answers)

	if (sID != -1): # -1 is a flag meaning there is no survey to immediately add it to
		append.master_survey(qID, sID)


#####################################################
# 			append.master_question()				#
#####################################################

def master_question(qID, question, answers):

	if(qID==""):
		errorMSG("append.master_question","No qID Provided")
		return
	if (question==""):
		errorMSG("append.master_question","No Question Provided")
		return

	answerStr = ""
	for ans in answers:
		if(ans!=""):
			if(answerStr==""):
				answerStr = answerStr+ans
			else:
				answerStr = answerStr+","+ans

	if(answerStr==""):
		errorMSG("append.master_question","No Answers Provided")
		return

	# write new row in order of qID, question, answers (in form id, question, ans1, ans2, ans3 etc.)
	with open('question_temp.csv','w+', newline = '') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([qID, question, answerStr])

	# overwrite master with changes and get rid of "" symbols
	try:
		with open('question_temp.csv') as csv_in, open('master_question.csv', 'a') as csv_out:
			for line in csv_in:
				csv_out.write(line.replace('\"',''))
		os.remove('question_temp.csv')
	except IOError:
		errorMSG("append.master_question","Error overwriting master with changes")
		return	



#####################################################
# 				append.master_survey()				#
#####################################################

def master_survey(qID, sID):

	if(qID==""):
		errorMSG("append.master_survey","No qID Provided")
		return
	if (sID==""):
		errorMSG("append.master_survey","No sID Provided")
		return

	# get current info in master_survey.csv file
	try:
		reader = csv.reader(open('master_survey.csv'))
	except IOError:
		errorMSG("append.master_survey","File master_survey.csv not found")
		return
	survey_list = []
	for row in reader:
		current_survey = {
			"surveyID":		row[0],
			"course": 		row[1],
			"date":  		row[2],
			"questionID":	row[3:],	
		}
		if (current_survey['surveyID'] == sID):
			if (qID not in current_survey['questionID']):
				current_survey['questionID'].append(qID)
		survey_list.append(current_survey)

	# the dicts at this stage are good for searching, sorting, modifying etc.
	# but need to reconvert list of questions into 1 string before re-writing to csv
	
	# convery questions list into string
	for survey in survey_list:
		line = ""
		for key,value in survey.items():
			if (key == 'questionID'):
				length = len(value)
				for i in range(0,length):
					line += str(value[i])
					if (i != length-1):
						line += ","
				survey['questionID'] = line

	# output new output to temporary file
	field_names = ['surveyID', 'course', 'date', 'questionID']
	with open('survey_temp.csv', 'w+') as csv_out:
		dict_writer = csv.DictWriter(csv_out, fieldnames = field_names)
		dict_writer.writerows(survey_list)

	# write from temp back to master_survey file to write in changes (without quotations)
	try:
		with open('survey_temp.csv') as csv_in, open('master_survey.csv', 'w') as csv_out:
			for line in csv_in:
				csv_out.write(line.replace('\"',''))
		os.remove('survey_temp.csv')
	except IOError:
		errorMSG("append.master_survey","Error overwriting master_survey file with changes")
		return	