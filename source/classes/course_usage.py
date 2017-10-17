import ast, os, time, copy
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from server import app, errorMSG
from defines import debug
from functions import get
from models import GeneralQuestion, MCQuestion, SurveyResponse,\
					GeneralResponse, MCResponse
from models import Survey, Course, UniUser
from database import db_session, Base
from flask_login import login_user, login_required, current_user, logout_user
from abc import ABCMeta, abstractmethod

class LoadCourse():
	'loads a specific survey'

	def load(id):
		course = Course.query.filter_by(id=id).first()		
		return course