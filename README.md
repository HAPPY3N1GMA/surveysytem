# COMP1531 Group Assignment

## Team

### 3N1GMA-HPY 		

### thequinneffect		

### RyanJE

### mkadeline	

Set Debug in Defines to ```True``` to drop and re-create all database tables

## Section 1:
Important packages and descriptions

Flask==0.12.2 - underlying CMS
Flask-Login==0.4.0 - Authorisation and Authentication of users
Flask-SQLAlchemy==2.2 - SQLAlchemy Flask extension
Jinja2==2.9.6 - Jinja2 templating for back end to front end data communication
matplotlib==1.5.1 - for charting of back end data on the front end
SQLAlchemy==1.1.14 - ORM for sqlite
SQLite==3.20.1 - database management system

For a full list of dependent packages, run ```pip install -r requirements.txt```



## Section 2:
Usage: Cd into ```/source``` and Run with ```python3 run.py```
Should you want to run with debuging stack traces printed to the browser, run ```python3 run.py --debug```

App available at ```http://127.0.0.1:5000```

## Section 3:
Testing can be done through the app via
- ```python3 run.py --testonly``` to run the unit tests and then exit
- ```python3 run.py --testfirst``` to run the unit tests and then run the app

or done through the external tests.py directory, by running ```python3 tests.py```
Tests included in tests.py are:
- question_create()
- question_edit()
- test_optional() to test optional and mandatory questions
- test_student_creation() 
- test_student_edit()
- test_staff_creation() 
- test_staff_edit()
- test_course_create()
- test_add_to_course() to test enrolling student and staff into a course
- survey_create_test() to test survey creation
- test_user_addition() to test adding users to a survey
- question_removal()
- test_response() to test the response to a survey


