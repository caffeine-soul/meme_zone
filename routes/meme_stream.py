import json
import uuid
import pyodbc
import pandas as pd
from config import config, db
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
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
            return redirect(url_for("routes.upload_page"))
        elif request.form.get("submit_btn") == "view":
            return redirect(url_for("routes.memes_get"))
        else:
            pass
    else:
        form = start_proc()
        return render_template("start.html", form=form)

@app.route("/home", methods=["GET", "POST"])
def upload_page():
    print("web/meme/upload_page")
    is_valid, form = meme_info()
    if request.method == "POST":
        is_valid, form = meme_info()
        if is_valid:
            uploader_name = form["uploader_name"].data
            meme_caption = form["meme_caption"].data
            meme_url = form["meme_url"].data
            another_entry_cb = form["another_entry_cb"].data
            meme_id = str(uuid.uuid4())
            insert_dttm = datetime.utcnow()
            try:
                db.meme_info.insert_one({ "uploader_name": uploader_name, "meme_caption": meme_caption,
                "meme_url": meme_url, "meme_id": meme_id, "insert_dttm": insert_dttm})
            except pyodbc.Error:
                return flask_api.status.HTTP_500_INTERNAL_SERVER_ERROR
            if another_entry_cb:
                flash("Uploaded Successfully!")
                return redirect(url_for("routes.upload_page"))
            else:
                return redirect(url_for("routes.memes_get"))
    else:
        return render_template("form.html", form=form)

@app.route("/", methods=["POST"])
@app.route("/memes", methods=["POST"])
def api_memes_post():
    data = request.get_json()
    uploader_name = data["name"]
    meme_caption = data["caption"]
    meme_url = data["url"]
    meme_id = str(uuid.uuid4())
    insert_dttm = datetime.utcnow() 
    try:
        db.meme_info.insert_one({ "uploader_name": uploader_name, "meme_caption": meme_caption,
        "meme_url": meme_url, "meme_id": meme_id, "insert_dttm": insert_dttm})
    except pyodbc.Error:
        return flask_api.status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify({"id": meme_id})

@app.route("/web/memes", methods=[ "GET"])
def memes_get():
    is_valid, form = meme_info()
    try:
        df = pd.DataFrame(db.meme_info.find({}, {"_id":0}).sort([("insert_dttm",-1)]).limit(100))
        meme_list = df.values.tolist()
    except pyodbc.Error:
        return flask.api.status.HTTP_500_INTERNAL_SERVER_ERROR
    return  render_template("index.html", len = len(meme_list), meme_list=meme_list) 

@app.route("/", methods=["GET"])
@app.route("/memes", methods=[ "GET"])
def api_memes_get():
    try:
        df = pd.DataFrame(db.meme_info.find({}, {"_id":0, "insert_dttm":0}).sort([("insert_dttm",-1)]).limit(100))
    except pyodbc.Error:
        return flask.api.status.HTTP_500_INTERNAL_SERVER_ERROR
    json_parsed = json.loads(df.to_json(orient="records"))
    return jsonify(json_parsed)


@app.route("/about", methods=["GET"])
def about():
    return "<h1>Crio Stage 2B submission by Krishna Maheshwari</h1>"


@app.route("/web/memes/<meme_id>", methods=["GET"])
def get_meme_by_id(meme_id):
    try:
        meme_url = db.meme_info.find_one({"meme_id":meme_id}, {"meme_url": 1})
    except pyodbc.Error:
        return flask.api.status.HTTP_500_INTERNAL_SERVER_ERROR
    return render_template("<img src="+ meme_url+ " alt='' style='width: 100%; height: auto;'>")


@app.route("/memes/<meme_id>", methods=["GET"])
def api_get_meme_by_id(meme_id):
    try:
        meme_dict = db.meme_info.find_one({"meme_id":meme_id}, {"_id":0})
    except pyodbc.Error:
        return flask.api.status.HTTP_500_INTERNAL_SERVER_ERROR
    json_object = json.dumps(meme_dict, indent = 4)
    return json_object