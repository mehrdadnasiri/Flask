from flask_restful import Resource

from authz.controller.apiv1 import AuthController

class AuthResource(Resource):
    def get(self):
        """
        GET/auth/tokens --> Verify the token.
        """
        return AuthController.verify_jwt_token()#verify the token

    def post(self):
        """
        POST /auth/tokens --> Create a new token. 
        """
        return AuthController.create_jwt_token() #create a new token.
