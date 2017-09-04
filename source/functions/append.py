import csv, ast, os
from classes import fileclasses
from functions import append
from server import errorMSG



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

	#(ast.literal_eval([answers]))
	print("TEMP:",answers)


	append.master_question(qID, question, answers)

	#mastercsv = fileclasses.csvfile("master_question.csv")

	#row = str(qID),question+"'"+','+str(answers)
	#print(row)

	#mastercsv.writetofile(row)


	#if (sID != -1): # -1 is a flag meaning there is no survey to immediately add it to
	#	append.master_survey(qID, sID)


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

	# FROM HERE NOT USED

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


	# TO HERE NOT USED 

	# write new row in order of qID, question, answers (in form id, question, ans1, ans2, ans3 etc.)
	with open('question_temp.csv','w+', newline = '') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([qID, question, answers])

	# overwrite master with changes and get rid of "" symbols
	try:
		with open('question_temp.csv') as csv_in, open('master_question.csv', 'a') as csv_out:
			for line in csv_in:
				line = line.replace(',[',',"[')
				line = line.replace(']\n',']"\n')
				#print(line.replace('\"','\"'))
				csv_out.write(line)
		os.remove('question_temp.csv')

		#write to answers master class

		answers = str(answers).replace(']', "")
		answers = str(answers).replace('[', "")
		#print(answers)
		fileclasses.question.create(qID, question, answers)


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
			"surveytitle":  row[1],
			"course": 		row[2],
			"date":  		row[3],
			"questionID":	row[4:],	
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
	field_names = ['surveyID', 'surveytitle','course', 'date', 'questionID']
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