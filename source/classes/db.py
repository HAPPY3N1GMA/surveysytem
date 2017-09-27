import sqlite3

"""
Precondition of running this program: 
Run Library.py for once
The MVC architecture which allows the 
user to query the library by book's name 
and also author's name

CREATE TABLE 
IF NOT EXISTS USERS
 (ID INTEGER NOT NULL,
 PASSWORD TEXT NOT NULL,
 NAME TEXT NOT NULL,
 ROLE TEXT);

CREATE TABLE 
IF NOT EXISTS QUESTIONS
(ID INT PRIMARY KEY NOT NULL,
QUESTION TEXT NOT NULL,
ANSWERS TEXT NOT NULL,
TYPE INTEGER NOT NULL,
STATUS INTEGER NOT NULL);

CREATE TABLE 
IF NOT EXISTS COURSES
 (ID INT PRIMARY KEY NOT NULL,
 QUESTION TEXT NOT NULL,
 ANSWERS TEXT NOT NULL,
 TYPE INTEGER NOT NULL,
 STATUS INTEGER NOT NULL);

CREATE TABLE 
IF NOT EXISTS RESULTS
 (ID INT PRIMARY KEY NOT NULL,
 ANSWERS TEXT NOT NULL);

CREATE TABLE 
IF NOT EXISTS SURVEYS
 (ID INT PRIMARY KEY NOT NULL,
 TITLE TEXT NOT NULL,
 COURSE INTEGER NOT NULL,
 DATE TEXT,
 QUESTIONS TEXT,
 STATUS INTEGER NOT NULL,
 RESULTS, INTEGER NOT NULL,
 FOREIGN KEY (COURSE) REFERENCES COURSES (ID),
 FOREIGN KEY (RESULTS) REFERENCES RESULTS (ID)
 );


"""


# Controller module
class Controller(object):
	def __init__(self):
		pass


###TEMP

	def search_table(self):
		model = LibraryModel()
		view = LibraryView()
		table = model.search_all()
		return view.print_table(table)


# Model
class LibraryModel(object):

############# temp to list the entire db ##################
	def search_all(self, author):
		query = "SELECT * from SURVEYS"
		db_list = self._dbselect(query)
		return db_list
###########################################################

	def search_all(self, author):
		query = "SELECT * from SURVEYS"
		db_list = self._dbselect(query)
		return db_list


	def _dbselect(self, query):
		#connect to db
		connection = sqlite3.connect('library.db')
		cursorObj = connection.cursor()
		# execute the query
		rows = cursorObj.execute(query)
		connection.commit()
		results = []
		for row in rows:
			results.append(row)
		cursorObj.close()
		return results

#View
class LibraryView(object):
	def table(self, table):
		print("The current DB is:")
		for row in table:
			print(row)
		print()



#Client Code
#controller = Controller()
#controller.search_author("Martin")
#controller.search_author("Tom")
#controller.search_book("Agile Design Principles")
#controller.search_book("The Lord of the Rings")
#controller.search_book("Pride and Prejudice")
#controller.search_book("The Great Gatsby")
#controller.search_book("Introduction to Cooking")