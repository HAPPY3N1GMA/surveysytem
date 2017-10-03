import csv, ast, os
from classes import fileclasses
from functions import append
from server import errorMSG

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