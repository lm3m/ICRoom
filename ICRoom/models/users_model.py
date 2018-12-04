import sys
import logging

from flask_restplus import fields
from api import api
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from auth import Authorization
from logs import log_debug

log = logging.getLogger(__name__)

# model for user creation
users_model = api.model('User', {
    'username': fields.String(required=True, description='Unique Username'), 
    'password': fields.String(required=True, description='Password')
})


class UsersModel(object):
    @staticmethod
    def user_exists(user_id):
        """
        checks if a given user exists for a given user id
        """
        user = redis.hget(user_id, "user")
        if user is not None:
            return True
        return False

    @staticmethod
    def build_user_id(username):
        """
        generate internal user id from username
        """
        return "user-{}".format(username)

    @staticmethod
    def create_user(username, password):
        """
        create a new user, making sure it username is unique
        """
        user_id = UsersModel.build_user_id(username)
        log_debug(log, user_id)

        if UsersModel.user_exists(user_id):
            raise BadRequest("User already exists")
        
        log_debug(log, "New User: {}".format(username))
        hashed = Authorization.hash_password(password)
        user_dict = {
            'user' : username,
            'password_hash' : str(hashed)
        }

        redis.hmset(user_id, user_dict)
        log_debug(log, redis.hgetall(user_id))
        return user_id

    @staticmethod
    def login(username, password):
        """
        logs the given user in and returns a jwt token
        """
        user_id = UsersModel.build_user_id(username)
        hashed = redis.hget(user_id, 'password_hash')
        if hashed is None or not Authorization.check_password(password, hashed):
            raise Unauthorized("username or password is not correct")
    
        return Authorization.encode_jwt_token(user_id)

    @staticmethod
    def logout(user, token):
        """
        logs the given user out and blocks the jwt token
        """
        Authorization.add_to_blocklist(token)
        return True

