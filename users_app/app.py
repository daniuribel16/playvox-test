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
from api.resources.user import User

# load environment variables file
dotenv_path = join(dirname(__file__), '../env')
load_dotenv(dotenv_path)

#api routes
def routes(api, db):
    api.add_resource(User, '/v1/users', '/v1/users/<string:id>',
        endpoint='user', resource_class_kwargs={'db': db})

# initialization of Flask Application
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['FLASK_APP'] = "users_app/app.py"
mongo = MongoDb(app, environ['USERS_DATABASE_NAME'])
db = mongo.getDb()
routes(Api(app), db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True, use_reloader=True)
