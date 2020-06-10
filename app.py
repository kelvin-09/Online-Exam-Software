from flask import Flask, render_template, url_for, request, flash, redirect
from forms import questionForm
from forms import paperForm
from flask_wtf import Form
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired
import sqlite3
import random
app = Flask(__name__)

app.secret_key = 'Secret'

@app.route('/createQuestion', methods = ['GET', 'POST'])
def question():
    form = questionForm()
    '''if request.method == 'POST':
        if form.validate() == False:
            flash("All fields are required")
            return "Errata"
            #return render_template('questionPage.html', form = form)
        else:
            return "success"
            #return redirect(url_for('submit'))
    return render_template('questionPage.html', form = form)'''
    return render_template('questionpage.html', form = form)
        
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
                flash("Duplicate Questions will not be inserted")
            c.execute("select * from question")
            conn.commit()
            questionLists = c.fetchall()
            conn.close()
            return render_template('qbpage.html', questionLists = questionLists)
        else:
            conn.close()
            return render_template('questionpage.html', form = form)
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
                flash("An error occured please try again")
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
        c.execute("delete from questionPaper where pid = ?", IDtuple)
        c.execute("delete from qset where pid = ?", IDtuple)
    except:
            flash("An error occured please try again")
    conn.commit()
    conn.close()
    return redirect('/questionpaper')

@app.route('/')
def homepage():
    return render_template('homepage.html')


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
            flash("Duplicate questions will not be added")
        conn.commit()
        conn.close()
        return redirect(url_for('viewPaper', id = id))


if __name__ == '__main__':
    app.run(debug=True)

