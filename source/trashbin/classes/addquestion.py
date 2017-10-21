    def addquestion(self):
        secCheck.authCheck()

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.addquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        question = request.form["question"]
        status = 0

        #by default a question is mandatory unless optional is checked
        if(request.form.getlist("optional")!=[]):
            status = 1

        if(question==""):
            common.Debug.errorMSG("append.question","No Question Provided")
            flash('Please Enter A Valid Question')
            return self.questioninfo()

        for text in question:
            if (get.cleanString(str(text))==False):
                common.Debug.errorMSG("routes.createsurvey","Invalid input in fields")
                flash('Invalid characters in question')
                return self.questioninfo()


        if(request.form["qtype"]=='0'):
            new = questions_model.GeneralQuestion(question,status)
            db_session.add(new)
            db_session.commit()
            return self.questioninfo()

        #multiple choice question
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
                return self.questioninfo()


        #if only one answer provided then return with error msg (this is not a valid question)
        if(len(answers)<2):
            common.Debug.errorMSG("routes.createsurvey","Only one answer provided for a mc question")
            flash("Multiple choice questions require atleast 2 answers")
            return self.questioninfo()

        new = questions_model.MCQuestion(question,answer_one,answer_two,answer_three,answer_four,status)
        db_session.add(new)
        db_session.commit()

        return self.questioninfo()

