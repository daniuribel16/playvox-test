from datetime import datetime
import json
from json import JSONEncoder
import pdb
from flask_restful import Resource
from flask import jsonify, request
from bson import json_util
from bson.objectid import ObjectId
from schema import Schema, And, Use

note_schema = Schema({'title': And(str),
                'body': And(str),
                'user_id': And(str)})

class UserNotes(Resource):

    error_resp = {'response': 'there was an error processing your request, check your parameters or try later'}

    # initialize db
    def __init__(self, **kwargs):
        self.db = kwargs['db']


    def get(self, id=None):
        user_id = ""
        try:
            # check if it was sent any query string params
            if request.args:
                user_id = request.args.get('user_id')
            
            # if it was sent a record id
            if id is not None:
                note = self.db.notes.find_one({"_id": ObjectId(id)})
                if note:
                    return json_util._json_convert(note)
                else:
                    return {"response": "no note found for {} id".format(id)}
            
            respond = []
            # if there are query params let's filter them
            if user_id:
                query = { "user_id": user_id }

                cursor = self.db.notes.find(query)
                for note in cursor:
                    noteObj = json_util._json_convert(note)
                    respond.append(noteObj)

                return { "notes": respond, "success": True }
            
            cursor = self.db.notes.find({})
            for user in cursor:
                userObj = json_util._json_convert(user)
                respond.append(userObj)

            return { "notes": respond, "success": True }
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp


    def post(self):
        try:
            data = request.get_json()
            if not note_schema.is_valid(data):
                return {
                    "response": "Bad request"
                }, 400

            note = {
                'title': str(data.get('title')),
                'body': str(data.get('body')),
                'user_id': str(data.get('user_id')),
                'created_at': datetime.utcnow()
            }
            
            inserted_note = self.db.notes.insert_one(note)
            
            return {
                "_id": str(inserted_note.inserted_id)
            }, 201
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp


    def put(self):
        try:
            data = request.get_json()
            if not data.get('_id'):
                return {
                    "response": "Bad request"
                }, 400

            data['updatedAt'] = datetime.utcnow()
            data['_id'] = ObjectId(data['_id'])
            q = {"_id": data['_id']}

            self.db.notes.update(q, {'$set': data})
            return json_util._json_convert(data)
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp


    def delete(self, id=None):
        try:
            # check if there is an id
            if id is not None:
                res = self.db.notes.delete_one({'_id': ObjectId(id)})
                print(res.deleted_count)
                return {"response": "{} documents deleted".format(res.deleted_count)}
            else:
                return {"response": "no id was provided"}
            
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp
