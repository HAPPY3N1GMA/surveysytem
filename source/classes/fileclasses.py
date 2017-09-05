import csv, ast, os, time
from defines import masterSurveys,masterQuestions,masterCourses
from shutil import copyfile
_masterSurveys = masterSurveys
_masterQuestions = masterQuestions
_masterCourses = masterCourses

#Classes for different file types
class IDfile():
	def __init__(self, filename):
		self._name = filename

class course(object):
	def __init__(self,courseName,offering):
		self.name = courseName
		self.offering = offering

	def create(courseName,offering):
		global _masterCourses
		newcourse = course(courseName,offering)
		#print(newquestion.answers)
		_masterCourses.append(newcourse)
		return newcourse

	#build list of courses
	def readall():
		global _masterCourses
		course_pool = []
		for course in _masterCourses:
			course_pool = course_pool + [[course.name,course.offering]]
		return course_pool

	def name(courseName):
		global _masterCourses
		for course in _masterCourses:
			if course.name == courseName:
				return course
		return 

	#return list of all course offerings
	def offering(courseOffering):
		global _masterCourses
		course_pool = []
		for course in _masterCourses:
			if course.offering == courseOffering:
				course_pool = course_pool + [[course.offering]]
		return course_pool

	#TODO: Add course object to survey class
	#TODO: Add question objects to survey class


class question(object):
	def __init__(self,questionID,questionName,answers):
		self.questionID = questionID
		self.questionName = questionName
		self.answers = answers

	def create(questionID,questionName,answers):
		global _masterQuestions
		newquestion = question(questionID,questionName,answers)
		#print(newquestion.answers)
		_masterQuestions.append(newquestion)
		return newquestion

	def qID(questionID):
		global _masterQuestions
		for question in _masterQuestions:
			if question.questionID == questionID:
				return question
		return 

	def list():
		global _masterQuestions
		question_pool = []
		for question in _masterQuestions:
			#correctly format the strings
			questionAnswers = str(question.answers)
			questionAnswers = ast.literal_eval(str(questionAnswers))
			question_pool = question_pool + [[question.questionID, question.questionName, questionAnswers]]

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

	def sID(surveyID):
		global _masterSurveys
		for survey in _masterSurveys:
			#print(survey.surveyID)
			if survey.surveyID == surveyID:
				return survey
		return None

	def read_all():
		global _masterSurveys
		survey_pool = []
		for survey in _masterSurveys:
			survey_pool = survey_pool + [[survey.surveyID, survey.surveyTitle, survey.courseName]]
			
		return survey_pool

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
	#this should be renamed as its specific to surveys nothing else
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

	def buildanswer(self,questions):
		with open(self._name,'a') as csv_out:
			writer = csv.writer(csv_out)
			writer.writerow(['question_id','answers'])
			for qID in questions:
				writer.writerow([qID,list()])



	#not used at this time
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