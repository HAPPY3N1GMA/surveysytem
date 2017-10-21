

    def modifyquestion(self):
        secCheck.authCheck()

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.modifyquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        oldType = request.form["oldType"] #old question type (was it MC or general?)
        qID = request.form["qID"]
        question = request.form["questiontitle"]

        status = 0

        if(request.form.getlist("optional")!=[]):
            status = 1

        #is the question getting deleted?
        if(request.form["delete"]=='1'):
            status = 2
        else:
            if(question==""):
                common.Debug.errorMSG("append.question","No Question Provided")
                flash('Please Enter A Valid Question')
                return self.questioninfo()

            for text in question:
                if (get.cleanString(str(text))==False):
                    common.Debug.errorMSG("routes.modifyquestion","Invalid input in fields")
                    flash('Invalid characters in question')
                    return self.openquestion()

        #open the correct question objecttype
        # 1 is MC, 2 is General
        if(oldType=='2'):
            qObject=questions_model.GeneralQuestion.query.filter_by(id=qID).first()
        else:
            qObject=questions_model.MCQuestion.query.filter_by(id=qID).first()  

        if(qObject==None):
            common.Debug.errorMSG("routes.modifyquestion ","No question object Found")
            return self.questioninfo()

        #is the question just getting deleted?
        if(status==2):
            qObject.status = status
            db_session.commit()
            return self.questioninfo()


        #extended response questions
        if(request.form["qtype"]=='0'):
            if(oldType=='2'):
                #same general type of question, just changing fields
                qObject.question = question
                qObject.status = status

            else:
                #change of question type - delete old type, and make new type
                qObject.status = 2
                new = questions_model.GeneralQuestion(question,status)
                db_session.add(new)
                
            db_session.commit() 

            return self.questioninfo()  


        #only multiple choice questions will get past here!

        answer_one = request.form["option_one"]
        answer_two = request.form["option_two"]
        answer_three = request.form["option_three"]
        answer_four = request.form["option_four"]

        #check for invalid characters
        answers = [answer_one,answer_two,answer_three,answer_four]
        answers = list(filter(None, answers))
        validStrings = copy.copy(answers)
        validStrings.append(question)


        for text in validStrings:
            if (get.cleanString(str(text))==False):
                common.Debug.errorMSG("routes.createsurvey","Invalid input in fields")
                flash('Invalid characters in answers')
                return self.openquestion()


        #if only one answer provided then return with error msg (this is not a valid question)
        if(len(answers)<2):
            common.Debug.errorMSG("routes.createsurvey","Multiple choice questions require atleast 2 answers")
            flash("Multiple choice questions require atleast 2 answers")
            return self.openquestion()

        #has by data type changed? If no, then I just update the MC fields
        if(oldType=='1'):
            qObject.question = question
            qObject.status = status
            qObject.answerOne = answer_one
            qObject.answerTwo = answer_two
            qObject.answerThree = answer_three
            qObject.answerFour = answer_four    
        else:
            #new mc question, set old question to deleted, and make new general question type
            qObject.status = 2
            new = questions_model.MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
            db_session.add(new)
        
        db_session.commit()

        return self.questioninfo()