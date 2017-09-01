
# 	answer Function temp readme
#	
#	appends a new answer result to a question for a specified survey
# 	
#	Note that this expects a survey file and will error if missing
#
# 	Example CSV File Format:
#
#	question_id,answers
#	1,"['a', 'a', 'b', 'b', 'c', 'a', 'd', 'j']"
#
# 	append.answer("test_answers","1","j") -- will open file test_answers.csv, 
# 	and append the answer j to question 1

import csv, ast, os

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

def answer(s_id, q_id, answer):
	file = str(s_id)+".csv"
	tmp = str(s_id)+"_tmp.csv"	
	with open(file, 'r+') as csvReadFile:
		fieldnames = ['question_id', 'answers']
		reader = csv.DictReader(csvReadFile, fieldnames=fieldnames)
		with open (tmp, 'w') as write_row:
			writer=csv.DictWriter(write_row, fieldnames=fieldnames)
			for row in reader:
				if(row['question_id']==q_id):
					tmp_list=ast.literal_eval(row['answers'])
					tmp_list.append(answer)
					row['answers'] = tmp_list
				writer.writerow(row)				
	os.remove(file)
	os.rename(tmp, file)


#####################################################
# 				append.question() 					#
#####################################################

def question(sID, question, answers): #assumes all params are strings

	master_question(qID, question, my_answers)

	if (sID != -1): # -1 is a flag meaning there is no survey to immediately add it to
		master_survey(qID, sID)


#####################################################
# 			append.master_question()				#
#####################################################

def master_question(qID, question, answers):

	# write new row in order of qID, question, answers (in form id, question, ans1, ans2, ans3 etc.)
	with open('question_temp.csv','w+', newline = '') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([qID, question, answers])

	# overwrite master with changes and get rid of "" symbols
	with open('question_temp.csv') as csv_in, open('master_question.csv', 'a') as csv_out:
		for line in csv_in:
			csv_out.write(line.replace('\"',''))


#####################################################
# 				append.master_survey()				#
#####################################################

def master_survey(qID, sID):

	# get current info in master_survey.csv file
	reader = csv.reader(open('master_survey.csv'))
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
	with open('survey_temp.csv') as csv_in, open('master_survey.csv', 'w') as csv_out:
		for line in csv_in:
			csv_out.write(line.replace('\"',''))