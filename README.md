# COMP1531 Group Assignment

## Team

### Keiran Sampson	-- 3N1GMA-HPY 		
Z5168147		

### Nicholas Quinn	--	thequinneffect		
Z5117408		

### Ryan Eves ---------	RyanJE
Z5164560		

### Matthew Adeline	--	mkadeline	
Z5157128		


TODO:

# W11 Iteration - Taken form Deliverables
1.  Features are to be implemented
    - **Complete** Implementation of security with three types of users (student, staff and admin) and display of
    appropriate dashboard depending upon the role of the user
    - **Complete** Use of database as the persistence layer to store all information (survey, questions, responses,
    credentials etc.)
    - Implementation of survey work-flow process as outlined in the requirements guidelines
        - **Complete** Admin creates survey in draft mode - not accessible by staff or students
        - **Complete** Staff review questions - [Add/Remove optional not required for It-2]
        - **Complete** Students fill out survey
        - **Complete** Admin closes survey - [Visualisation not required]
    - **Complete** Multiple response types for questions
    - Optional questions **not** required for this iteration
    - Visualisation of survey results is **not** required for this iteration
2. Document artifacts
    - An updated list of user-stories along with key acceptance criteria to comply with the revised
    project specification. Some of these acceptance criteria will need to be transformed into test-cases
    for iteration 3.
    - A revised conceptual class diagram with attributes only.
    - A sequence diagram to capture survey workflow process (This could be done as four separate
    sequence diagrams to show (a) survey creation by admin (b) survey review by staff (c) survey filled
    out by student (d) survey closure by admin

# W13 Iteration
Students and staff will be able to get access to a graphical display of survey results only after the survey
has closed. 




# Misc
**we need to put this in! not just wipe the db everytime**
changes to any csv file will be added to db automatically on startup!
 

**our survey staff can still see the survey questions, but modifying/publishing is disabled**
**see comment in routes.py line 400ish**
 Survey appears on the dashboard of all staff associated with the course offering, but as soon as
one staff reviews it, it disappears from the dashboard of other staff associated with the course. 

**atm ours is only set by the admin publishing it....and then ending the survey**
reviewed by the staff-in-charge, the survey should be active (i.e. open to the
students) only for a fixed period of time. Once, the period lapses, students should no longer be able to
fill out the survey.




### password etc
50,staff670,staff
50,COMP4931,18s1


### STAFF ID
1161,SENG2011,17s2
1161,staff1161,staff


### STUDENT ID
298,SENG2011,17s2
298,student763,student

