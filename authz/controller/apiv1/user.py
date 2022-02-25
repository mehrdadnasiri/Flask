from flask import request

from authz.authz import db
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.util import user_expires_at, jsonify, now

class UserController:

    def get_users():
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)#invalid media type
        try:
            users = User.query.all()
        except Exception as e:
            return jsonify(status=500, code=102)#database error
        users_schema = UserSchema(many=True)
        return jsonify(
            {"users": users_schema.dump(users)}
        ) 

    def get_user(user_id):
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)#invalid media type
        try:
            user= User.query.get(user_id)#find the user
        except Exception as e:
            return jsonify(status=500, code=102)#database error
        if user is None :
            return jsonify (status=404, code=103)#User is not found
        user_schema = UserSchema()
        return jsonify(
            {"user":user_schema.dump(user)}
        )

    def create_user(): 
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)#invalid media type
        user_schema = UserSchema(only=["username", "password"])
        try:
            user_data = user_schema.load(request.get_json()) #Read and validate user data
        except Exception as e:
            return jsonify(status=400, code=104)
        if not user_data.get("username") or not user_data.get("password"):
            return jsonify(status=400, code=105)#empty data
        try:
            user = User.query.filter_by(username=user_data.get("username")).first()
        except Exception as e:
            return jsonify(status=500, code=102)#database error
        if user is not None:
            return jsonify(status=409, code=106)#User is already exist.
        user = User(
            username=user_data.get("username"), 
            password=user_data.get("password")
        )#create new user
        db.session.add(user)
        try:
            db.session.commit() #Execute INSERT command.
        except Exception as e:
            db.session.rollback()
            return jsonify(status=500 , code=102)#Database error
        user_schema = UserSchema()
        return jsonify(
            {"user": user_schema.dump(user)}, status=201
        )

    def update_user(user_id):
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)#invalid media type
        user_schema =UserSchema(only=["password"], unknown="include")
        try:
            user_data = user_schema.load(request.get_json())#Read and validate user data.
        except Exception as e:
            return jsonify(status=400, code=104)
        if len(user_data) != 2:
            return jsonify(status=400, code=104)
        if "password" not in user_data or "oldpassword" not in user_data:
            return jsonify(status=400, code=104)
        if not user_data.get("password") or not user_data.get("oldpassword"):
            return jsonify(status=400, code=105)#empty data
        try:
            user= User.query.get(user_id)#find the user
        except Exception as e:
            return jsonify(status=500, code=102)#database error
        if user is None :
            return jsonify (status=404, code=103)#User is not found
        if user.password != user_data.get("oldpassword"):
            return jsonify(status=403, code=111)
        
        user.password = user_data.get("password") #set a new password
        user.expires_at = user_expires_at()
        user.last_change_at = now()
        user.failed_auth_at = None
        user.failed_auth_count= 0
        try:
            db.session.commit() #Execute Update command.
        except Exception as e:
            db.session.rollback()
            return jsonify(status=500 , code=102)#Database error
        user_schema = UserSchema()
        return jsonify(
            {"user": user_schema.dump(user)}
        )

    def delete_user(user_id):
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)#invalid media type
        try:
            user= User.query.get(user_id)#find the user
        except Exception as e:
            return jsonify(status=500, code=102)#database error
        if user is None :
            return jsonify (status=404, code=103)#User is not found
        db.session.delete(user)
        try:
            db.session.commit() #Execute DELETE command.
        except Exception as e:
            db.session.rollback()
            return jsonify(status=500 , code=102)#Database error 
        return jsonify()#user was deleted successfuly
        