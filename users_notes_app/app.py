# -*- coding: utf-8 -*-
import sys
import os
from os import environ
from flask import Flask, render_template, jsonify, url_for, redirect, request, Blueprint
from flask_restful import Api, Resource
from flask_cors import CORS
from os.path import join, dirname
from dotenv import load_dotenv

from common.mongoDB import MongoDb
from api.resources.user_notes import UserNotes

dotenv_path = join(dirname(__file__), '../env')
load_dotenv(dotenv_path)

def routes(api, db):
    api.add_resource(UserNotes, '/v1/user_notes', '/v1/user_notes/<string:id>',
        endpoint='user_notes', resource_class_kwargs={'db': db})

# initialization of Flask Application
app = Flask(__name__)
app.config['FLASK_APP'] = "users_notes_app/app.py"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mongo = MongoDb(app, environ['USER_NOTES_DATABASE_NAME'])
db = mongo.getDb()
routes(Api(app), db)

@app.route('/')
def Index():
    return render_template('../static/index/public/index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True, use_reloader=True)
