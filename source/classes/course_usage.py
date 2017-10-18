from models import Course
from abc import ABCMeta, abstractmethod

class LoadCourse():
	'loads a specific course'
	def load(id):	
		return Course.query.filter_by(id=id).first()