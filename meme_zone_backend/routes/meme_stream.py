import json
import uuid
import pandas as pd
from config import config, db
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from flask import Flask, render_template, flash, request
from datetime import datetime

from . import routes as app


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
    except:
        return flask_api.status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify({"id": meme_id})

@app.route("/", methods=["GET"])
@app.route("/memes", methods=[ "GET"])
def api_memes_get():
    try:
        df = pd.DataFrame(db.meme_info.find({}, {"_id":0, "insert_dttm":0}).sort([("insert_dttm",-1)]).limit(100))
    except:
        return flask.api.status.HTTP_500_INTERNAL_SERVER_ERROR
    json_parsed = json.loads(df.to_json(orient="records"))
    return jsonify(json_parsed)


@app.route("/memes/<meme_id>", methods=["GET"])
def api_get_meme_by_id(meme_id):
    try:
        meme_dict = db.meme_info.find_one({"meme_id":meme_id}, {"_id":0})
    except pyodbc.Error:
        return flask.api.status.HTTP_500_INTERNAL_SERVER_ERROR
    json_object = json.dumps(meme_dict, indent = 4)
    return json_object