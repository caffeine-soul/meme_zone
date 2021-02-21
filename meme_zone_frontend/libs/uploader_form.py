from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import ValidationError, DataRequired, URL

class UploaderForm(FlaskForm):
    uploader_name = TextField("Name: ", [DataRequired()])
    meme_caption = TextAreaField("Caption: ", [DataRequired()])
    meme_url = TextField("URL: ", [DataRequired(), URL()])
    another_entry_cb = BooleanField("Upload another meme")
    submit = SubmitField("Submit!")
def meme_info():
    form = UploaderForm()
    return form
