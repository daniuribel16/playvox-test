from datetime import datetime
import json
from json import JSONEncoder
import pdb
from flask_restful import Resource
from flask import jsonify, request
from bson import json_util
from bson.objectid import ObjectId
from schema import Schema, And, Use

user_schema = Schema({'name': And(str),
                'last_name': And(str),
                'email': And(str),
                'gender': And(str),
                'age': And(int)})

class User(Resource):

    error_resp = {'response': 'there was an error processing your request, check your parameters or try later'}

    # initialize db
    def __init__(self, **kwargs):
        self.db = kwargs['db']


    def get(self, id=None):
        data = ""
        page = ""
        limit = ""
        try:
            # check if it was sent any query string params
            if request.args:
                data = request.args.get('query')
                page = request.args.get('page')
                limit = request.args.get('limit')

            # if it was sent a record id
            if id is not None:
                user = self.db.user.find_one({"_id": ObjectId(id)})
                if user:
                    return { "users": json_util._json_convert(user), "count": 1, "success": True }
                else:
                    return {"response": "no user found for {} id".format(id)}
            
            respond = []
            # if there are query params let's filter them
            if data:
                params = json.loads(data)
                query = {
                    "$or": [
                        {"name": params.get('name') if 'name' in params else '' },
                        {"last_name": params.get('last_name') if 'last_name' in params else ''},
                        {"age": params.get('age') if 'age' in params else ''},
                        {"gender": params.get('gender') if 'gender' in params else ''},
                        {"email": params.get('email') if 'email' in params else ''}
                    ]
                }

                cursor = self.db.user.find(query)
                count = cursor.count()
                # check if it need to be paginated
                if page and limit:
                    cursor = cursor.skip((int(page) - 1) * int(limit)).limit(int(limit))

                for user in cursor:
                    userObj = json_util._json_convert(user)
                    respond.append(userObj)

                return { "users": respond, "count": count, "success": True }
            
            cursor = self.db.user.find({})
            count = cursor.count()

            # check if it need to be paginated
            if page and limit:
                cursor = cursor.skip((int(page) - 1) * int(limit)).limit(int(limit))

            for user in cursor:
                userObj = json_util._json_convert(user)
                respond.append(userObj)

            return { "users": respond, "count": count, "success": True }
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp


    def post(self):
        try:
            data = request.get_json()
            if not user_schema.is_valid(data):
                return {
                    "response": "Bad request"
                }, 400

            # check if user is already registered
            cursor = self.db.user.find({'email': data.get('email')})
            if cursor.count() > 0:
                return {"response": "Email {} already registered".format(data.get('email'))}
            
            user = {
                'name': str(data.get('name')),
                'last_name': str(data.get('last_name')),
                'email': str(data.get('email')),
                'age': str(data.get('age')),
                'gender': str(data.get('gender')),
                'created_at': datetime.utcnow()
            }
            inserted_user = self.db.user.insert_one(user)
            
            return {
                "_id": str(inserted_user.inserted_id)
            }, 201
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp


    def put(self):
        try:
            data = request.get_json()
            data['updatedAt'] = datetime.utcnow()
            data['_id'] = ObjectId(data['_id'])
            q = {"_id": data['_id']}

            self.db.user.update(q, {'$set': data})
            return json_util._json_convert(data)
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp


    def delete(self, id=None):
        try:
            # check if there is an id
            if id is not None:
                res = self.db.user.delete_one({'_id': ObjectId(id)})
                print(res.deleted_count)
                return {"response": "{} documents deleted".format(res.deleted_count)}
            else:
                return {"response": "no id was provided"}
            
        except Exception as e:
            print("error: {}".format(e))
            return self.error_resp
