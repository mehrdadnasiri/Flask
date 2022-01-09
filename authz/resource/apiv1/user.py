from flask_restful import Resource

from authz.controller.apiv1 import UserController

class UserResource(Resource):

    def get(self , user_id=None):
        """
        GET /users ---> Get list of users .
        GET /users/<user_id>---> Get user.
        """
        if user_id is None:
            return UserController.get_users()
        else:
            return UserController.get_user(user_id)
        
    def post(self):
        """
        POST /users ---> Create new user .
        POST /users/<user_id>---> Not Allowed.
        """        
        return UserController.create_user() #Create new user
    def patch(self, user_id):
        """
        PATCH /users ---> Not Allowed .
        PATCH /users/<user_id>---> Update user.
        """
        return UserController.update_user(user_id)#Update user
    def delete(self, user_id):
        """
        DELETE /users ---> Not Allowed .
        GET /users/<user_id>---> Delete user.
        """
        return UserController.delete_user(user_id)#Delete user
