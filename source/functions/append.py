
# 	append_answer Function temp readme
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
