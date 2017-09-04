import csv, ast, os, time
from defines import masterSurveys,masterQuestions
_masterSurveys = masterSurveys
_masterQuestions = masterQuestions

#Classes for different file types
class IDfile():
	def __init__(self, filename):
		self._name = filename


class question(object):
	def __init__(self,questionID,questionName,answers):
		self.questionID = questionID
		self.questionName = questionName
		self.answers = answers

	def create(questionID,questionName,answers):
		global _masterQuestions
		newquestion = question(questionID,questionName,answers)
		print(newquestion.answers)
		_masterQuestions.append(newquestion)
		return newquestion

	def read(questionID):
		global _masterQuestions
		for question in _masterQuestions:
			if question.questionID == questionID:
				return question
		return 

	def readall():
		global _masterQuestions
		question_pool = []
		for question in _masterQuestions:
			#correctly format the strings
			questionAnswers = str(question.answers)
			questionAnswers = ast.literal_eval(str(questionAnswers))
			question_pool = question_pool + [[question.questionID,question.questionName,questionAnswers]]

		return question_pool

class survey(object):
	def __init__(self,surveyID,surveyTitle,courseName,date,questionList):
		self.surveyID = surveyID
		self.surveyTitle = surveyTitle
		self.courseName = courseName
		self.date = date
		self.questionList = ast.literal_eval(str(questionList))

	def create(surveyID,surveyTitle,courseName,date,questionList):
		global _masterSurveys
		newsurvey = survey(surveyID,surveyTitle,courseName,date,questionList)
		_masterSurveys.append(newsurvey)
		return newsurvey

	def read(surveyID):
		global _masterSurveys
		for survey in _masterSurveys:
			print(survey.surveyID)
			if survey.surveyID == surveyID:
				return survey
		return None

#class for textfiles, accessing mainly ID files
class textfile(IDfile):
	def getcurrentID(self):
		try:
			fileID = open(self._name,"r+")
		except FileNotFoundError:
			return 0
		else:
			val = fileID.read()
			if val == '':
				val = 0
			fileID.close()
			return str(val)
	def updateID(self):
		new_val = int(self.getcurrentID())
		IDfile = open(self._name,"w")
		new_val += 1
		IDfile.write(str(new_val))
		return str(new_val)

#Writing to and from CSV files
class csvfile(IDfile):
	def writeto(self,ID,name,course,time,questions):
		with open(self._name,'a') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow([ID,name,course,time,list(questions)])
		#add to masterSurvey classlist
		survey.create(ID,name,course,time,questions)
	def readfrom(self):
		with open(self._name,'r') as csv_in:
			next(csv_in) #skip header line
			reader = csv.reader(csv_in)
			namelist = []
			for row in reader:
				namelist.append(row)
			return namelist
	def readfromid(self,rowID):
		file = self.readfrom()
		for row in file:
			if row[0]==str(rowID):
				return row

	def appendfield(self,rowID,fieldID,content):
		tmp = "tmp.csv"
		with open(self._name, 'r+') as csvReadFile:
			reader = csv.DictReader(csvReadFile)
			with open (tmp, 'w') as write_row:
				#get list of fields from the csv header
				fields = reader.fieldnames;
				#rowIDField is always the first field/column
				rowIDField = fields[0]
				writer=csv.DictWriter(write_row, fieldnames=fields)
				writer.writeheader() #write headerfiles
				for row in reader:
					if(row[rowIDField]==rowID):
						tmp_list=ast.literal_eval(row[fieldID])
						tmp_list.append(content)
						row[fieldID] = tmp_list
					writer.writerow(row)				
		os.remove(self._name)
		os.rename(tmp, self._name)

	def readDict(self):
		with open(self._name, 'r+') as csvReadFile:
			reader = csv.DictReader(csvReadFile)
			#get list of fields from the csv header
			fields = reader.fieldnames;
			tmp = []
			output = []
			for row in reader:
				for field in fields:
					tmp = tmp + list([row[field]])
				output = output+[tmp]
			#result = str(output).replace('"', "")
			#print(result)
			return output