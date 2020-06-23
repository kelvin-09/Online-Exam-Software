from flask import Flask, render_template, url_for, request, flash, redirect, session, json, Response
from forms import questionForm
from forms import paperForm, scheduleForm
from flask_wtf import Form
from flask_ckeditor import CKEditor
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired
import sqlite3
import random
import re
import datetime
from camera import VideoCamera
import numpy as np
import os
import cv2
import cameratest
app = Flask(__name__)

ckeditor = CKEditor(app)
app.secret_key = 'Secret'

@app.route('/createQuestion', methods = ['GET', 'POST'])
def question():
    form = questionForm()
    return render_template('questionPage.html', form = form)
        
@app.route('/submit')
def submit():
    return "Question created"

@app.route('/questionbank', methods = ['POST', 'GET'])
def questionbank():
    form = questionForm()  
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    if request.method == 'POST':
        if form.validate():
            questionDetailList = []
            questionDetailList.append(form.question.data)
            questionDetailList.append(form.keywords.data)
            questionDetailList.append(form.keySentences.data)
            questionDetailList.append(form.marks.data)
            questionDetailList.append(form.difficulty.data)
            questionDetailList.append(form.topic.data)
            questionDetailList.append(form.subject.data)
            questionDetailTuple = tuple(questionDetailList)
            try: 
                c.execute('''insert into question(question, keywords, keySentences, marks, difficulty, topic, subject) 
                values(?, ?, ?, ?, ?, ?, ?)''', questionDetailTuple)
            except:
                flash("")
            c.execute("select * from question")
            conn.commit()
            questionLists = c.fetchall()
            conn.close()
            return render_template('qbpage.html', questionLists = questionLists)
        else:
            conn.close()
            return render_template('questionPage.html', form = form)
    else:
        c.execute("select * from question")
        questionLists = c.fetchall()
        conn.close()
        return render_template('qbpage.html', questionLists = questionLists)
    

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    IDtuple = (id,) #(value, ) is a tuple while (value) is not a tuple
    try: 
        c.execute("delete from question where qid = ?", IDtuple)
        c.execute("delete from qset where qid = ?", IDtuple)
    except:
            flash("An error occured please try again")
    conn.commit()
    conn.close()
    return redirect('/questionbank')


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    form = questionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            questionDetailList = []
            questionDetailList.append(form.question.data)
            questionDetailList.append(form.keywords.data)
            questionDetailList.append(form.keySentences.data)
            questionDetailList.append(form.marks.data)
            questionDetailList.append(form.difficulty.data)
            questionDetailList.append(form.topic.data)
            questionDetailList.append(form.subject.data)
            questionDetailList.append(id)
            questionDetailTuple = tuple(questionDetailList)
            try:
                c.execute('''update question set question = ?, keywords = ?, keySentences = ?,
            marks = ?, difficulty = ?, topic = ?, subject = ? where qid = ?''',questionDetailTuple)
            except:
                flash("An error occured please try again")
            conn.commit()
            return redirect(url_for('questionbank'))
        else:
            return render_template('update.html', form = form, id = id)
    else:
        IDtuple = (id,)
        c.execute("select * from question where qid = ?", IDtuple)
        updateQuestion = c.fetchone()
        form.question.data = updateQuestion[1]
        form.keywords.data = updateQuestion[2]
        form.keySentences.data = updateQuestion[3]
        form.marks.data = updateQuestion[4]
        form.difficulty.data = updateQuestion[5]
        form.topic.data = updateQuestion[6]
        form.subject.data = updateQuestion[7]
        form.submit.label.text = 'Update Question'
        return render_template('update.html', form = form, id = id)


@app.route('/questionpaper', methods = ['POST', 'GET'])
def questionpaper():
    form = paperForm() 
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    if request.method == 'POST':
        if form.validate_on_submit():
            questionPaperList = []
            questionPaperList.append(form.name.data)
            questionPaperList.append(form.duration.data)
            questionPaperList.append(0)
            questionPaperTuple = tuple(questionPaperList)
            try:
                c.execute('''insert into questionPaper(name, duration, maxMarks) 
                values(?, ?, ?)''', questionPaperTuple)
            except:
                flash("")
            c.execute("select * from questionPaper")
            c.execute("select * from questionPaper")
            questionPaperLists = c.fetchall()
            for paper in questionPaperLists:
                c.execute(''' select sum(p.marks) from qset q, question p where pid = ? and q.qid = p.qid''', (paper[0],))
                m = c.fetchall()[0][0]
                c.execute("update questionpaper set maxmarks = ? where pid = ?", (m, paper[0]))
            c.execute("select * from questionPaper")
            conn.commit()
            questionPaperLists = c.fetchall()
            conn.close()
            return render_template('questionpaper.html', questionPaperLists = questionPaperLists)
        else:
            return render_template('qpaperPage.html', form = form)
    else:
        c.execute("select * from questionPaper")
        questionPaperLists = c.fetchall()
        try:
            for paper in questionPaperLists:
                c.execute(''' select sum(p.marks) from qset q, question p where pid = ? and q.qid = p.qid''', (paper[0],))
                m = c.fetchall()[0][0]
                c.execute("update questionpaper set maxmarks = ? where pid = ?", (m, paper[0]))
        except:
                flash("An error occured please try again")
        c.execute("select * from questionPaper")
        questionPaperLists = c.fetchall()
        conn.close()
        return render_template('questionpaper.html', questionPaperLists = questionPaperLists)

@app.route("/createPaper", methods = ['GET','POST'])
def createPaper():
    form = paperForm()
    return render_template('qpaperPage.html', form = form)


@app.route('/delete/paper/<int:id>')
def deletePaper(id):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    IDtuple = (id,) #(value, ) is a tuple while (value) is not a tuple
    try:
        c.execute("delete from testSchedule where name in (select name from questionPaper where id = ?)", IDtuple)
        c.execute("delete from questionPaper where pid = ?", IDtuple)
        c.execute("delete from qset where pid = ?", IDtuple)
    except:
            flash("An error occured please try again")
    conn.commit()
    conn.close()
    return redirect('/questionpaper')



@app.route('/view/paper/<int:id>', methods = ['GET', 'POST'])
def viewPaper(id):
    if request.method == 'GET':
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute("select * from questionPaper where pid = ?", (id,))
        paperDetail = c.fetchall()
        
        IDtuple = (id,)
        c.execute("select qid from qset where pid = ?", IDtuple)
        qIDList = []
        for qList in c.fetchall():
            qIDList.append(qList[0])
        questionDetailList = []
        for qid in qIDList:
            c.execute("select * from question where qid = ?", (qid,))
            questionDetailList.append(c.fetchone())
            
        marks = 0
        if len(questionDetailList) > 0:
            for q in questionDetailList:
                marks += q[4]
        conn.close()
        return render_template("setQuestionPaper.html", questionDetailList = questionDetailList, id = id, paperDetail = paperDetail, marks = marks)

@app.route('/random/<int:id>', methods = ['GET', 'POST'])
def randomfun(id):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    c.execute("select qid from qset where pid = ?", (id,))
    qIDList = []
    for qList in c.fetchall():
        qIDList.append(qList[0])
    c.execute("select qid from question")
    qBankList = []
    for qList in c.fetchall():
        qBankList.append(qList[0])
    availQuestionList = []
    for qid in qBankList:
        if qid not in qIDList:
            availQuestionList.append(qid)
    if len(availQuestionList) < 1:
        flash("No question left to add")
        conn.close()
        return redirect(url_for('viewPaper',id = id))
    else:
        addID = random.choice(availQuestionList)
        try:
            c.execute("insert into qset values (?, ?)", (id, addID))
        except:
            flash("An error occured please try again")
        conn.commit()
        conn.close()
        return redirect(url_for('viewPaper',id = id))

@app.route('/remove/<int:pid>/<int:qid>', methods = ['GET', 'POST'])
def remove(pid, qid):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    try:
        c.execute("delete from qset where pid = ? and qid = ?", (pid, qid))
    except:
            flash("An error occured please try again")
    conn.commit()
    conn.close()
    return redirect(url_for('viewPaper', id = pid))


@app.route('/questionbank/view/<int:id>', methods = ['GET', 'POST'])
def viewqb(id):
    if request.method == 'POST':
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute("select * from question")
        questionLists = c.fetchall()
        conn.close()
        return render_template('viewquestionbank.html', questionLists = questionLists, id = id)

@app.route('/back/<int:id>', methods = ['GET', 'POST'])
def back(id):
    return redirect(url_for('viewPaper', id = id))


@app.route('/choose/<int:id>', methods = ['GET', 'POST'])
def choose(id):
    if request.method == 'POST':
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute("select * from question where qid not in(select qid from qset where pid = ?)", (id, ))
        questionLists = c.fetchall()
        conn.close()
        if len(questionLists) < 1:
            flash("No question left to add")
            return redirect(url_for('viewPaper', id = id))
        else:
            return render_template('chooseQuestions.html', questionLists = questionLists, id = id)

@app.route('/chooseQuestions/<int:id>', methods = ['GET', 'POST'])
def chooseQuestions(id):
    if request.method == "POST":
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute("select qid from question")
        idLIST = c.fetchall()
        try:
            for listID in idLIST:
                if request.form.get(str(listID[0])) == "1":
                    c.execute("insert into qset values(?, ?)", (id, listID[0]))
        except:
            flash("An error Occured Please try again!")
        conn.commit()
        conn.close()
        return redirect(url_for('viewPaper', id = id))

@app.route('/schedule', methods = ['GET', "POST"])
def schedule():
    form = scheduleForm()
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    if request.method == 'POST':
        testList = []
        testList.append(form.testName.data)
        testList.append(form.start.data)
        testList.append(form.end.data)
        testTuple = tuple(testList)
        try:
            c.execute('''insert into testSchedule(name, start, end) values(?, ?, ?)''', testTuple)
        except:
            flash("")
        conn.commit()
        c.execute("select * from testSchedule")
        testLists = c.fetchall()
        tempList = []
        for test in testLists:
            temp = []
            temp.append(test[0])
            temp.append(test[1])
            temp.append(datetime.datetime.strptime(test[2], '%Y-%m-%d %H:%M:%S').strftime("%d %b, %Y      %H:%M %p"))
            temp.append(datetime.datetime.strptime(test[3], '%Y-%m-%d %H:%M:%S').strftime("%d %b, %Y      %H:%M %p"))
            tempList.append(temp)
        testLists = tempList
        conn.close()
        return render_template('scheduleTest.html', testLists = testLists)
    else:
        c.execute("select * from testSchedule")
        testLists = c.fetchall()
        tempList = []
        for test in testLists:
            temp = []
            temp.append(test[0])
            temp.append(test[1])
            temp.append(datetime.datetime.strptime(test[2], '%Y-%m-%d %H:%M:%S').strftime("%d %b, %Y      %H:%M %p"))
            temp.append(datetime.datetime.strptime(test[3], '%Y-%m-%d %H:%M:%S').strftime("%d %b, %Y      %H:%M %p"))
            tempList.append(temp)
        testLists = tempList
        conn.close()
        return render_template('scheduleTest.html', testLists = testLists)


@app.route('/scheduleTest', methods = ['GET', 'POST'])
def scheduleTest():
    form = scheduleForm()
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    c.execute('select name from questionPaper where name not in (select name from testSchedule)')
    testList = []
    for test in c.fetchall():
        testList.append((test[0], test[0]))
    form.testName.choices = testList
    if len(testList) < 1:
        flash("No tests left to schedule")
    conn.close()
    return render_template('scheduleForm.html', form = form)


@app.route('/delete/schedule/<int:id>')
def deleteSchedule(id):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    IDtuple = (id,)
    try:
        c.execute("delete from testSchedule where tid = ?", IDtuple)
    except:
            flash("An error occured please try again")
    conn.commit()
    conn.close()
    return redirect('/schedule')

@app.route('/testpage', methods = ['GET', 'POST'])
def testpage():
    #cameratest.breakLoop = True
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    c.execute("select * from testSchedule")
    testList = c.fetchall()
    tempList = []
    for test in testList:
        temp = []
        temp.append(test[0])
        temp.append(test[1])
        temp.append(datetime.datetime.strptime(test[2], '%Y-%m-%d %H:%M:%S').strftime("%d %b, %Y      %H:%M %p"))
        temp.append(datetime.datetime.strptime(test[3], '%Y-%m-%d %H:%M:%S').strftime("%d %b, %Y      %H:%M %p"))
        tempList.append(temp)
    testList = tempList
    newtestList = []
    for test in testList:
        test = list(test)
        c.execute('''select pid from questionPaper where name = ?''', (test[1], ))
        a = c.fetchall()
        c.execute(''' select count(*) from qset where pid = ?''', (a[0][0], ))
        a = c.fetchall()
        test.append(a[0][0])
        c.execute("select duration from questionPaper where name = ?", (test[1], ))
        a = c.fetchall()
        test.append(a[0][0])
        newtestList.append(test)
    testList = newtestList
    conn.close()
    return render_template('studentTest.html', testList = testList)

@app.route('/test/<int:id>', methods = ['GET', 'POST'])
def test(id):
    if request.method == 'POST':
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute("select start, end from testSchedule where tid = ?", (id, ))
        temp = c.fetchall()
        startTime = datetime.datetime.strptime(temp[0][0], '%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(temp[0][1], '%Y-%m-%d %H:%M:%S')
        currTime = datetime.datetime.now()
        if currTime >= startTime and currTime <= endTime:
            #cameratest.breakLoop = False
            #cameratest.record()
            return redirect(url_for('testhome', QID = 0, TID = id))
        else:
            flash("The Test has not started or it has expired.")
            return redirect(url_for('testpage'))
        

@app.route('/test/question/<int:TID>/<int:QID>', methods = ['GET', 'POST'])
def testhome(TID, QID):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    answerList = []
    sid = 2
    c.execute("select start, end from testSchedule where tid = ?", (TID, ))
    testDetails = c.fetchall()[0]
    c.execute('''select * from questionPaper where 
            name = (select name from testSchedule where tid = ?)''', (TID, ))
    paperDetail = c.fetchall()[0]
    c.execute(''' select qid from qset where pid = ?''', (paperDetail[0], ))
    Qid = []
    for q in c.fetchall():
        Qid.append(q[0])
    for id in Qid:
        c.execute("select ans from answers where sid = ? and tid = ? and qid = ?", (sid, TID, id))
        temp = c.fetchall()
        if temp:
            answerList.append(temp[0][0])
        else:
            answerList.append("Write your answer here...")
    Qid = tuple(Qid)
    questionDetail = []
    for id in Qid:
        c.execute(''' select question, marks from question where qid = ? ''', (id, ))
        questionDetail.append(c.fetchall()[0])
    if questionDetail == []:
        flash("No questions in this test")
        return redirect(url_for('testpage'))
    else:
        startTime = datetime.datetime.strptime(testDetails[0], '%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(testDetails[1], '%Y-%m-%d %H:%M:%S')
        testDetails = list(testDetails)
        testDetails[0] = startTime.timestamp() * 1000
        testDetails[1] = endTime.timestamp() * 1000
        testDetail = json.dumps(testDetails)
        conn.close()
        return render_template('testPaper.html', QID = QID, paperDetail = paperDetail, questionDetail = questionDetail, TID = TID, answerList = answerList, testDetail = testDetail)    
    

@app.route('/save/<int:TID>/<int:QID>', methods = ['GET', 'POST'])
def save(TID, QID):
    conn = sqlite3.connect("questionBank.db")
    c = conn.cursor()
    #sid = session['id']
    sid = 2
    answerList = []
    c.execute("select start, end from testSchedule where tid = ?", (TID, ))
    testDetails = c.fetchall()[0]
    c.execute('''select * from questionPaper where 
            name = (select name from testSchedule where tid = ?)''', (TID, ))
    paperDetail = c.fetchall()[0]
    c.execute(''' select qid from qset where pid = ?''', (paperDetail[0], ))
    Qid = []
    for q in c.fetchall():
        Qid.append(q[0])
    Qid = tuple(Qid)
    questionDetail = []
    for id in Qid:
        c.execute(''' select question, marks from question where qid = ? ''', (id, ))
        questionDetail.append(c.fetchall()[0])
    answer = request.form.get('ckeditor')
    c.execute("select ans from answers where sid = ? and tid = ? and qid = ?", (sid, TID, Qid[QID]))
    if c.fetchall():
        c.execute("update answers set ans = ? where sid = ? and tid = ? and qid = ?", (answer, sid, TID, Qid[QID]))
    else:
        c.execute(''' insert into answers (sid, tid, qid, ans, marks) 
        values(?, ?, ?, ?, ?) ''', (sid, TID, Qid[QID], answer, questionDetail[QID][1]))
    conn.commit()
    for id in Qid:
        c.execute("select ans from answers where sid = ? and tid = ? and qid = ?", (sid, TID, id))
        temp = c.fetchall()
        if temp:
            answerList.append(temp[0][0])
        else:
            answerList.append("Write your answer here...")
    startTime = datetime.datetime.strptime(testDetails[0], '%Y-%m-%d %H:%M:%S')
    endTime = datetime.datetime.strptime(testDetails[1], '%Y-%m-%d %H:%M:%S')
    testDetails = list(testDetails)
    testDetails[0] = startTime.timestamp() * 1000
    testDetails[1] = endTime.timestamp() * 1000
    testDetail = json.dumps(testDetails)
    conn.close()
    return render_template('testPaper.html', QID = QID, paperDetail = paperDetail, questionDetail = questionDetail, TID = TID, answerList = answerList, testDetail = testDetail) 


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('base.html')

@app.route('/loginStudent', methods = ['GET', 'POST'])
def loginStudent():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute('SELECT * FROM studentDetails WHERE username = ? AND password = ?', (username, password,))
        account = c.fetchone()
        conn.close()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]
            return redirect(url_for('testpage'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('loginStudentPage.html', msg=msg)


@app.route('/loginTeacher', methods = ['GET', 'POST'])
def loginTeacher():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute('SELECT * FROM teacherDetails WHERE username = ? AND password = ?', (username, password,))
        account = c.fetchone()
        conn.close()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]
            return render_template('homepage.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template('loginTeacherPage.html', msg=msg)


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('base.html')

@app.route('/registerTeacher', methods = ['GET', 'POST'])
def registerTeacher():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute('SELECT * FROM teacherDetails WHERE username = ?', (username,))
        account = c.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            c.execute('INSERT INTO teacherDetails (name, username, email, password) values (?, ?, ?, ?)', (name, username, email, password))
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('registerTeacherPage.html', msg=msg)

@app.route('/registerStudent', methods = ['GET', 'POST'])
def registerStudent():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = sqlite3.connect("questionBank.db")
        c = conn.cursor()
        c.execute('SELECT * FROM studentDetails WHERE username = ?', (username,))
        account = c.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            c.execute('INSERT INTO studentDetails (sname, username, email, password) values (?, ?, ?, ?)', (name, username, email, password))
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('registerStudentPage.html', msg=msg)

@app.route('/studentHome', methods = ['GET', 'POST'])
def studentHome():
    return render_template("")

@app.route('/teacherHome', methods = ['GET', 'POST'])
def teacherHome():
    return render_template('homepage.html')


@app.route('/recording')
def index():
    return cameratest.record()


    

if __name__ == '__main__':
    app.run(debug=True)

