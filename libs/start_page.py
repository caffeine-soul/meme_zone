from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import ValidationError, DataRequired, URL

class StartForm(FlaskForm):
    upload = SubmitField()
    view = SubmitField()
def start_proc():
    form = StartForm()
    return form
