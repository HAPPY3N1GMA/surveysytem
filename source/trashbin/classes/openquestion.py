    def openquestion(self):
        secCheck.authCheck()

        if(current_user.role != 'Admin'):
            common.Debug.errorMSG("routes.openquestion","unauthorised user attempted access:",current_user.id)
            return render_template("home.html", user=current_user)

        if (request.form.getlist('question')==[]):
            flash('No question selected')
            common.Debug.errorMSG("routes.openquestion","question not selected")
            return self.questioninfo()      

        qID = request.form['question']
        questionType = 1

        #load up the question from db
        if (qID[1:2]=='0'): 
            questionObject = questions_model.MCQuestion.query.filter_by(id=int(qID[4:5])).first()
        elif (qID[1:2]=='1'):
            questionObject = questions_model.GeneralQuestion.query.filter_by(id=int(qID[4:5])).first()
            questionType = 2 #so we know if question type was modified in form
        if (questionObject==None):
            common.Debug.errorMSG("routes.openquestion","This question does not exist")
            return self.questioninfo()

        return render_template("modifyquestion.html",user=current_user,questionObject=questionObject,questionType=questionType)
