from flask import request
from jwt import encoded, decode

from authz.util import jsonify
class AuthController:

    def create_jwt_token():
        return jsonify(status=501, code=107)#Not Implemented
    
    def verify_jwt_token():
        return jsonify(status=501, code=107)#Not Implemented
