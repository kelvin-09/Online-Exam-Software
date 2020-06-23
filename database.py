import sqlite3
conn = sqlite3.connect("questionBank.db")
c = conn.cursor()

#c.execute(''' create table teacherDetails(id integer primary key autoincrement,
#             name text not null, username text not null unique, email text not null unique, password text not null) ''')


#c.execute(''' create table answers(aid integer primary key autoincrement, 
#            sid integer not null, tid integer not null,
#            qid integer not null, ans text not null, marks real default 0, 
#            constraint fk1 foreign key(sid) references studentDetails(sid), 
#            constraint fk2 foreign key(tid) references testSchedule(tid),
#            constraint fk3 foreign key(qid) references question(qid)) ''')

#c.execute(''' create table studentDetails(sid integer primary key autoincrement,
#             sname text not null, username text not null unique, email text not null unique, password text not null) ''')
#
#c.execute('''create table testSchedule(tid integer primary key autoincrement,
#            name text not null unique, start text not null, end text not null,
#             constraint fk foreign key(name) references questionPaper(name))''')

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
