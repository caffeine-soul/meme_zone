import json
import uuid
import pandas as pd
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from libs.uploader_form import meme_info
from libs.start_page import start_proc
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, validators, SubmitField, TextAreaField
from datetime import datetime

from . import routes as app


@app.errorhandler(404)
def not_found(e): 
    return render_template("404.html") 

@app.route("/start", methods=["GET", "POST"])
def start_page():
    if request.method == "POST":
        form = start_proc()
        render_template("start.html", form=form)
        if request.form.get("submit_btn") == "upload":
            return redirect(url_for("routes.memes", start_page_var="True"))
        elif request.form.get("submit_btn") == "view":
            return redirect(url_for("routes.memes", start_page_var="False"))
        else:
            pass
    else:
        form = start_proc()
        return render_template("start.html", form=form)


@app.route("/", methods=["POST", "GET"])
@app.route("/memes", methods=["POST", "GET"])
def memes():
    form = meme_info()
    if request.method == "POST":
        if form.validate_on_submit():
            uploader_name = form["uploader_name"].data
            meme_caption = form["meme_caption"].data
            meme_url = form["meme_url"].data
            another_entry_cb = form["another_entry_cb"].data

            headers = {
            'Content-Type': 'application/json',
            }
            json_data = { 
            'name': uploader_name, 'caption': meme_caption, 'url': meme_url
            }
            json_object = json.dumps(json_data, indent=4)  
            response = requests.post('https://meme-zone-v1.herokuapp.com/', headers= headers, data=json_object)
            if another_entry_cb:
                flash("Uploaded Successfully!")
                return redirect(url_for("routes.memes", start_page_var="True"))
            else:
                return redirect(url_for("routes.memes", start_page_var="False"))
        else:
            return render_template("form.html", form=form)
    else:
        if request.args.get('start_page_var')=="True":
            return render_template("form.html", form=form)
        else:
            form = meme_info()
            data_raw = requests.get('https://meme-zone-v1.herokuapp.com/')
            return  render_template("index.html", meme_list=data_raw.json())


@app.route("/about", methods=["GET"])
def about():
    return "<h1>Created with <3 by Krishna Maheshwari!</h1>"


@app.route("/memes/<string:meme_id>", methods=["GET"])
def get_meme_by_id(meme_id):
    meme_info = requests.get('https://meme-zone-v1.herokuapp.com/memes/'+meme_id)
    meme_url = meme_info.json()["meme_url"]
    return "<center> <img src="+ meme_url + " style='width: 100%; height: auto;'></center>"

