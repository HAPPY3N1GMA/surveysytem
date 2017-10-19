
from abc import ABCMeta, abstractmethod
from models import users_model, surveys_model, questions_model, courses_model

class LoadCourse():
	'loads a specific course'
	def load(id):	
		return courses_model.Course.query.filter_by(id=id).first()