import unittest
from database import init_db
from database_loader import DB_Loader
from classes import unit_tests
from datetime import datetime
from flask import Flask
from flask_login import LoginManager
from models import users_model, questions_model, surveys_model, courses_model
from classes.authenticate import Credentials, LoginSuccess, LoginFailure
from classes import survey_usage
from database import db_session
from sqlalchemy import exc


class TestRunner(unittest.TestCase):

	def __init__(self):
		self.q_tests = QuestionTest()
		self.stu_tests = StudentTest()
		self.sta_tests = StaffTest()
		self.co_tests = CourseUnitTest()
		self.su_tests = SurveyTest()
		self.res_tests = ResponseTest()
		self.clean = TestCleanup()

	def run(self):
        db_load = DB_Loader()
        init_db()
        db_load.db_load()
		print("----------------------------------------------------------")
		print("                 Commencing Unit Testing                  ")
		print("----------------------------------------------------------")
		
		self.q_tests.question_create()
		self.q_tests.question_edit()
		self.q_tests.test_optional()
		self.stu_tests.test_student_creation()
		self.stu_tests.test_student_edit()
		self.sta_tests.test_staff_creation()
		self.sta_tests.test_staff_edit()
		self.co_tests.test_course_create()
		self.co_tests.test_add_to_course()
		self.su_tests.survey_create_test()
		self.su_tests.test_user_addition()
		self.su_tests.question_removal()
		self.res_tests.test_response()
		print("----------------------------------------------------------")
		print("        Testing Complete - Cleaning Up Test Cases         ")
		print("----------------------------------------------------------")
		self.clean.cleanup_all()

		print("----------------------------------------------------------")
		print("                   Finished Unit Testing                  ")
		print("----------------------------------------------------------")


class QuestionTest(unittest.TestCase):

	def question_create(self):
		mcquestion = questions_model.MCQuestion("UnitTest MC Question", "1", "2", "3", "4", 0)
		genquestion = questions_model.GeneralQuestion("UnitTest General Question", 0)
		mcquestion_man = questions_model.MCQuestion("UnitTest Man MC Question", "1", "2", "3", "4", 1)
		genquestion_man = questions_model.GeneralQuestion("UnitTest Man General Question", 1)
		db_session.add(mcquestion)
		db_session.add(genquestion)
		db_session.add(mcquestion_man)
		db_session.add(genquestion_man)
		db_session.commit()

		# Test existence
		_mcquestion = questions_model.MCQuestion.query.filter_by(question="UnitTest MC Question").first()
		assert _mcquestion.answerOne == "1"
		assert _mcquestion.answerTwo == "2"
		assert _mcquestion.answerThree == "3"
		assert _mcquestion.answerFour == "4"
		_genquestion = questions_model.GeneralQuestion.query.filter_by(question="UnitTest General Question").first()
		assert _genquestion is not None
		_genquestion_man = questions_model.GeneralQuestion.query.filter_by(question="UnitTest Man General Question").first()
		assert _genquestion_man is not None
		_mcquestion_man = questions_model.MCQuestion.query.filter_by(question="UnitTest Man MC Question").first()
		assert _mcquestion_man is not None

	def question_edit(self):
		mcquestion = questions_model.MCQuestion.query.filter_by(question="UnitTest MC Question").first()
		genquestion = questions_model.GeneralQuestion.query.filter_by(question="UnitTest General Question").first()
		genquestion.question = "UnitTest GenQuestion Edit"
		mcquestion.question = "UnitTest MCQuestion Edit"
		mcquestion.answerOne = "5"
		mcquestion.answerTwo = "6"
		mcquestion.answerThree = "7"
		mcquestion.answerFour = "8"
		db_session.commit()

		# Test edits
		_mcquestion_real = questions_model.MCQuestion.query.filter_by(question="UnitTest MCQuestion Edit").first()
		_genquestion_real = questions_model.GeneralQuestion.query.filter_by(question="UnitTest GenQuestion Edit").first()
		assert _genquestion_real is not None
		assert _mcquestion_real.answerOne == "5"
		assert _mcquestion_real.answerTwo == "6"
		assert _mcquestion_real.answerThree == "7"
		assert _mcquestion_real.answerFour == "8"

	def test_optional(self):
		print("------------------------------")
		print(">>>> Testing Optional and Mandatory Questions\n")

		_genquestion_man = questions_model.GeneralQuestion.query.filter_by(question="UnitTest Man General Question").first()
		_mcquestion_man = questions_model.MCQuestion.query.filter_by(question="UnitTest Man MC Question").first()
		_mcquestion_real = questions_model.MCQuestion.query.filter_by(question="UnitTest MCQuestion Edit").first()
		_genquestion_real = questions_model.GeneralQuestion.query.filter_by(question="UnitTest GenQuestion Edit").first()
		self.assertEqual(_genquestion_real.status, 0)
		self.assertEqual(_mcquestion_real.status, 0)
		self.assertEqual(_genquestion_man.status, 1)
		self.assertEqual(_mcquestion_man.status, 1)

		print("<<<<< Optional Question Testing Passed")
		print("------------------------------")


class StudentTest(unittest.TestCase):

	def test_student_creation(self):
		print("------------------------------")
		print("Testing Student Creation and Saving\n")
		print(">>>> Testing Invalid Student Creation and Saving")
		student = users_model.Student("", "passwordUT", "Student", [], [])
		try:
			db_session.add(student)
			db_session.commit()
		except exc.SQLAlchemyError:
			print("Test Passed\n")
			db_session.rollback()

		print(">>>> Testing Valid Student Creation and Saving")
		student = users_model.Student("12345", "passwordUT", "Student", [], [])
		db_session.add(student)
		db_session.commit()


		# Test existence
		_student = users_model.Student.query.get(12345)
		assert _student is not None
		assert _student.password == "passwordUT"
		assert _student.role == "Student"
		print(">>>> Test Passed\n")

	def test_student_edit(self):
		print(">>>> Testing Valid Student Edit and Saving")
		_student = users_model.Student.query.get(12345)
		_student.password = "passwordEditUT"
		db_session.commit()
		print(">>>> Test Passed\n")

		# Test Edit
		student = users_model.Student.query.get(12345)
		assert (student.password == "passwordEditUT"), student.password
		print("<<<<< All Student Creation Tests Passed")
		print("------------------------------")


class StaffTest(unittest.TestCase):

	def test_staff_creation(self):
		print("------------------------------")
		print("Testing Student Creation and Saving\n")
		print(">>>> Testing Invalid Staff Creation and Saving")
		staff = users_model.Staff("", "passwordUT", "Staff", [], [])
		try:
			db_session.add(staff)
			db_session.commit()
		except exc.SQLAlchemyError:
			print(">>>> Test Passed\n")
			db_session.rollback()

		staff = users_model.Staff("23456", "passwordUT", "Staff", [], [])
		db_session.add(staff)
		db_session.commit()

		# Save existence
		_staff = users_model.Staff.query.get(23456)
		assert _staff is not None
		assert _staff.password == "passwordUT"
		assert _staff.role == "Staff"

	def test_staff_edit(self):
		print(">>>> Testing Invalid Staff Editing and Saving")
		_staff = users_model.Staff.query.get(23456)
		_staff.password = "passwordEditUT"
		db_session.commit()

		# Test Edit
		staff = users_model.Staff.query.get(23456)
		assert staff.password == "passwordEditUT"
		print(">>>> Test Passed\n")
		print("<<<<< All Student Creation Tests Passed")
		print("------------------------------")


class CourseUnitTest(unittest.TestCase):

	def test_course_create(self):
		course = courses_model.Course("UTCourse17", "18s1", [])
		db_session.add(course)
		db_session.commit()

		# Test Existence
		_course = courses_model.Course.query.filter_by(name="UTCourse17").first()
		assert _course is not None
		assert _course.offering == "18s1"

	def test_add_to_course(self):
		print("------------------------------")
		print(">>>> Testing Enrollent of Student into Course\n")
		_student = users_model.Student.query.get(12345)
		assert _student is not None
		_staff = users_model.Staff.query.get(23456)
		assert _staff is not None

		_course = courses_model.Course.query.filter_by(name="UTCourse17").first()
		_student.courses.append(_course)
		_staff.course.append(_course)
		db_session.commit()

		# Test Addition
		student = users_model.Student.query.get(12345)
		assert student is not None
		self.assertTrue(student.courses)
		self.assertEqual(student.courses[0].id, _course.id)
		print("<<<< Student Successfully enrolled in course")
		print("------------------------------")
		staff = users_model.Staff.query.get(23456)
		assert staff is not None
		self.assertTrue(staff.courses)

class SurveyTest(unittest.TestCase):

	def survey_create_test(self):
		print("------------------------------")
		print("Testing Create a survey\n")

		# Set up tests using passed tests
		_course = courses_model.Course.query.filter_by(name="UTCourse17").first()
		assert _course is not None
		_mcquestion_real = questions_model.MCQuestion.query.filter_by(question="UnitTest MCQuestion Edit").first()
		_genquestion_real = questions_model.GeneralQuestion.query.filter_by(question="UnitTest GenQuestion Edit").first()
		assert _genquestion_real is not None
		assert _mcquestion_real is not None

		mc_questions = []
		gen_questions = []
		mc_questions.append(_mcquestion_real)
		gen_questions.append(_genquestion_real)

		print(">>>> Testing Create survey with no title")
		try:
			if not survey_usage.CreateSurvey.err_check('', _course.id,'2017/10/23', '2017/10/30'):
				print(">>>> Test Passed\n")
		except:
			print(">>>> Test Passed\n")
		print(">>>> Testing Create survey with no course")
		try:
			survey_usage.CreateSurvey.err_check('title', '','2017/10/23', '2017/10/30')
		except:
			print(">>>> Test Passed\n")

		print(">>>> Testing Create valid survey")	
		survey = surveys_model.Survey("Unit Test Survey", _course.id, [], [], [])
		start = datetime(2017,10,23)
		end = datetime(2017,10,23)
		survey.set_dates(start, end)
		survey.mc_questions.append(_mcquestion_real)
		survey.gen_questions.append(_genquestion_real)
		
		db_session.add(survey)

		db_session.commit()

		# Test Creation 
		_survey = surveys_model.Survey.query.filter_by(title="Unit Test Survey").first()
		assert _survey is not None
		self.assertTrue(_survey.mc_questions)
		self.assertTrue(_survey.gen_questions)
		assert _survey.course_id == _course.id
		print(">>>> Test Passed\n")

	def test_user_addition(self):
		print(">>>> Testing Create valid survey")	
		survey = surveys_model.Survey.query.filter_by(title="Unit Test Survey").first()
		assert survey is not None
		survey.add_staff()
		survey.add_students()
		db_session.commit()

		# Test addition
		_survey = surveys_model.Survey.query.filter_by(title="Unit Test Survey").first()
		self.assertTrue(_survey.users)
		print(">>>> Test Passed\n")

	def question_removal(self):
		print(">>>> Testing Create valid survey")	
		_survey = surveys_model.Survey.query.filter_by(title="Unit Test Survey").first()

		for question in _survey.mc_questions:
			if question.question == "UnitTest GenQuestion Edit":
				_survey.mc_questions.remove(question)

		# Test Removal
		self.assertEqual(len(_survey.mc_questions), 1)
		print(">>>> Test Passed\n")
		print("<<<< Survey Testing Passed all Tests")
		print("------------------------------")


class ResponseTest(unittest.TestCase):

	def test_response(self):
		print("------------------------------")
		print(">>>> Testing Survey Response\n")
		_survey = surveys_model.Survey.query.filter_by(title="Unit Test Survey").first()
		_mcquestion = questions_model.MCQuestion.query.filter_by(question="UnitTest MCQuestion Edit").first()
		_genquestion = questions_model.GeneralQuestion.query.filter_by(question="UnitTest GenQuestion Edit").first()

		surveyResp = surveys_model.SurveyResponse(_survey.id)
		db_session.add(surveyResp)

		response_gen_cont = "test response"
		gen_response = questions_model.GeneralResponse(surveyResp.id, _genquestion.id, response_gen_cont)
		surveyResp.gen_responses.append(gen_response)
		response_mc_cont = "A"
		mc_response = questions_model.MCResponse(surveyResp.id, _mcquestion.id, response_mc_cont)
		surveyResp.mc_responses.append(mc_response)

		db_session.commit()

		# Test Creation
		_surveyResp = surveys_model.SurveyResponse.query.filter_by(survey_id=_survey.id).first()
		assert _surveyResp is not None
		self.assertTrue(_surveyResp.mc_responses)
		self.assertTrue(_surveyResp.gen_responses)
		print("<<<< Survey Response Testing Passed all Tests")
		print("------------------------------")

class TestCleanup(unittest.TestCase):
	
	def cleanup_all(self):
		_mcquestion_real = questions_model.MCQuestion.query.filter_by(question="UnitTest MCQuestion Edit").first()
		_genquestion_real = questions_model.GeneralQuestion.query.filter_by(question="UnitTest GenQuestion Edit").first()
		_student = users_model.Student.query.get(12345)
		_staff = users_model.Staff.query.get(23456)
		_course = courses_model.Course.query.filter_by(name="UTCourse17").first()
		_survey = surveys_model.Survey.query.filter_by(title="Unit Test Survey").first()
		_surveyResp = surveys_model.SurveyResponse.query.filter_by(survey_id=_survey.id).first()
		_gen_response = questions_model.GeneralResponse.query.filter_by(response_id=_surveyResp.id).first()
		_mc_response = questions_model.MCResponse.query.filter_by(response_id=_surveyResp.id).first()
		_genquestion_man = questions_model.GeneralQuestion.query.filter_by(question="UnitTest Man General Question").first()
		_mcquestion_man = questions_model.MCQuestion.query.filter_by(question="UnitTest Man MC Question").first()

		# Clean up the many to many relationships
		_course.uniusers = []
		_survey.users = []
		_survey.mc_questions = []
		_survey.gen_questions = []
		_student.surveys = []

		db_session.delete(_survey)
		db_session.delete(_genquestion_real)
		db_session.delete(_mcquestion_real)
		db_session.delete(_staff)
		db_session.delete(_student)
		db_session.delete(_gen_response)
		db_session.delete(_mc_response)
		db_session.delete(_surveyResp)
		db_session.delete(_course)
		db_session.delete(_genquestion_man)
		db_session.delete(_mcquestion_man)

		db_session.commit()

		# Test Deletion
		student = users_model.Student.query.get(12345)
		assert student is None
		staff = users_model.Staff.query.get(23456)
		assert staff is None
		mcquestion_real = questions_model.MCQuestion.query.filter_by(question="UnitTest MCQuestion Edit").first()
		assert mcquestion_real is None
		genquestion_real = questions_model.GeneralQuestion.query.filter_by(question="UnitTest GenQuestion Edit").first()
		assert genquestion_real is None
		course = courses_model.Course.query.filter_by(name="UTCourse17").first()
		assert course is None
		survey = surveys_model.Survey.query.filter_by(title="Unit Test Survey").first()
		assert survey is None
		surveyResp = surveys_model.SurveyResponse.query.filter_by(survey_id=_survey.id).first()
		assert surveyResp is None
		gen_response = questions_model.GeneralResponse.query.filter_by(response_id=_surveyResp.id).first()
		assert gen_response is None
		mc_response = questions_model.MCResponse.query.filter_by(response_id=_surveyResp.id).first()
		assert mc_response is None

if __name__=="__main__":
	runner = TestRunner()
	runner.run()