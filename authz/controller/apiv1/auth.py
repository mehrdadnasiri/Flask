from flask import request
from jwt import encoded, decode
from time import time

from authz.authz import db
from authz.config import Config
from authz.model import User
from authz.schema.apiv1 import UserSchema
from authz.util import jsonify, now
class AuthController:

    def create_jwt_token():
        if request.content_type != "application/json":
            return jsonify(status=415, code=101)#invalid media type
        user_schema = UserSchema(only=["username","password"])
        try:
            user_data = user_schema.load(request.get_json())
        except:
            return jsonify(status=400, code=104)
        if not user_data.get("username") or not user_data.get("password"):
            return jsonify(status=400, code=105)
        try:
            user = User.query.filter_by(username=user_data.get("username")).first() #Finde the user
        except:
            return jsonify(status=500, code=102)#database error
        if user is None:
            return jsonify(status=401, code=103)
        if user.password != user_data.get("password"):
            user.failed_auth_at = now()
            user.failed_auth_count +=1
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify(status=500 ,code=101)#database error
            return jsonify(status=401, code=111) #invalide password
        if user.expires_at < now():
            return jsonify(status=401, code=108)# user is expired 
        if user.status != Config.USER_ALL_STATUS
            return jsonify(status=401 ,code=109)#bad user status
        current_time = time()
        try:
            user_jwt_token = encode(
                {
                    "sub": user.id,
                    "exp": current_time + Config.USER_DEFAULT_TOKEN_EXPIRY_TIME,
                    "nbf": current_time,
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role,
                    } 
                },
                Config.SECRET_KEY,
                config.JWT_ALGO
            ).encode("utf8") #Create JWT Token
        except:
            return jsonify(status=500, code=110) #token encryption error
        user.last_login_at= now()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(status=500, code=102)#database error 
        user_schema= UserSchema()
        return jsonify(
            state= {user_schema.dump(user)},
            headers={"X-Subject-Token": user_jwt_token}
        ) #return jwt token in addition to  user info 

    def verify_jwt_token():
        return jsonify(status=501, code=107)#Not Implemented

