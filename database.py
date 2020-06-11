import sqlite3
conn = sqlite3.connect("questionBank.db")
c = conn.cursor()
c.execute("delete from qset")
'''c.execute("select qid from qset where pid = ?", 1)
qIDList = []
for qList in c.fetchall():
    qIDList.append(qList[0])
questionDetailList = []
for qid in qIDList:
    c.execute("select * from question where qid = ?", (qid,))
    questionDetailList.append(c.fetchone())
print(questionDetailList)'''
#from csv import reader
#opened_file = open('test1.csv')
#read_file = reader(opened_file)
#qList = list(read_file)
#for q in qList:
#  c.execute('''insert into question (question, keywords, keySentences, marks,
#          difficulty, topic, subject) values(?, ?, ?, ?, ?, ?, ?)''', tuple(q))

#c.execute('''create table qset(pid integer not null, qid integer not null, 
#           constraint pk primary key(pid, qid), constraint fk1 foreign key(pid) references questionPaper(pid),
#           constraint fk2 foreign key(qid) references question(qid))''')
#c.execute('''create table question(qid integer primary key autoincrement,
#           question text not null unique, keywords text, keySentences text,
#          marks integer not null, difficulty integer not null,
#         topic text not null, subject text not null)''')
#c.execute("create table questionPaper(pid integer primary key autoincrement, name text not null unique, duration integer not null, maxMarks integer default 0)")
conn.commit()
conn.close()
