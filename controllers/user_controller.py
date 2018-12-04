import logging

from flask import request, make_response, jsonify
from flask_restplus import Resource, fields
from rest_plus import api
from models.users_model import UsersModel, users_model
from werkzeug.exceptions import HTTPException, BadRequest
from auth import Authorization

log = logging.getLogger(__name__)

prefix = api.namespace('users', description='Controller for Users')


@prefix.route('/')
class UsersController(Resource):
    @prefix.doc('Create a new user')
    @prefix.expect(users_model, validate=True)
    def post(self):
        """
        creates a new user
        """
        return UsersModel.create_user(api.payload['username'], api.payload['password']), 200


@prefix.route('/<username>')
@prefix.param('username', 'user to act upon')
class UserController(Resource):
    @prefix.doc('User actions: login, logout')
    def patch(self, username):
        """
        actions for users: login, logout
        """
        action = request.args.get('action')
        if action is None:
            raise BadRequest("No action query parameter")
        
        if action == "login":
            auth_token = UsersModel.login(username, api.payload['password'])
            response_object = { 'auth_token': auth_token }
            return response_object, 200
        elif action == "logout":
            token = Authorization.get_auth_token(request.headers)
            user = Authorization.validate_decode_token(token)
            return UsersModel.logout(user, token), 200
        else:
            raise BadRequest("\'{}\' is not a valid action.".format(action))

