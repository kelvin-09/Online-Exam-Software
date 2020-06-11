from flask import Flask
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SubmitField, TextAreaField, SelectField, RadioField, FieldList, FormField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, DataRequired

class questionForm(Form):
    question = TextAreaField("Enter a Question", validators= [InputRequired("Question field is required"), DataRequired()], default="Write a Question...")
    keywords = TextAreaField("Enter keywords(as csv)", validators=[InputRequired("Keywords field is required")])
    keySentences = TextAreaField("Enter key-sentences(as csv)", validators=[InputRequired("Key-sentences field is required")])
    topic = TextField("Topic", validators=[InputRequired("Topic field is required")])
    difficulty = SelectField("Difficulty", choices = [('1', 'Level 1'), ('2', 'Level 2'), ('3', 'Level 3')])
    marks = IntegerField("Marks", validators=[InputRequired("Marks field is required")])
    subject = TextField("Subject", validators=[InputRequired("Subject field is required")])
    submit = SubmitField("Create question")
    #locations = FieldList(TextField("Location"), min_entries=2, max_entries=4)

class paperForm(Form):
    name = TextField("Enter question paper name", validators=[InputRequired()])
    duration = IntegerField("Duration of the paper (in minutes)", validators=[InputRequired()])
    submit = SubmitField("Submit")