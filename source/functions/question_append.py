import csv

def append_question(sID, question, answers): #assumes all params are strings

	append_master_question(qID, question, my_answers)

	if (sID != -1): # -1 is a flag meaning there is no survey to immediately add it to
		append_master_survey(qID, sID)

#####################################################

def append_master_question(qID, question, answers):

	# write new row in order of qID, question, answers (in form id, question, ans1, ans2, ans3 etc.)
	with open('question_temp.csv','w+', newline = '') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([qID, question, answers])

	# overwrite master with changes and get rid of "" symbols
	with open('question_temp.csv') as csv_in, open('master_question.csv', 'a') as csv_out:
		for line in csv_in:
			csv_out.write(line.replace('\"',''))

#####################################################

def append_master_survey(qID, sID):

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