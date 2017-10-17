# abstract
class SurveyStatus:
	__metaclass__ = ABCMeta

	@abstractmethod
	def execute(user):
		pass

class StatusModify(SurveyStatus):
	'purpose: '

	def execute(self):
		general = GeneralQuestion.query.all()
        multi = MCQuestion.query.all()

        surveygen = survey.gen_questions
        surveymc = survey.mc_questions

        return render_template("modifysurvey.html",user=current_user,
			surveygen=surveygen,surveymc=surveymc,survey=survey,
			course=course,general=general,multi=multi)

class StatusAnswer(SurveyStatus):
	'purpose: '

	def execute(self):
		return render_template("answersurvey.html", survey=survey,
                                       course=course)

class StatusResults(SurveyStatus):
	'purpose: '

	def execute(self):
		pass

class StatusError(SurveyStatus):
	'purpose: '

	def execute(self):
		return self.surveyinfo()