import sys
import logging

from flask_restplus import fields
from rest_plus import api
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from auth import Authorization

log = logging.getLogger(__name__)

# model for user creation
users_model = api.model('User', {
    'username': fields.String(required=True, description='Unique Username'), 
    'password': fields.String(required=True, description='Password')
})

class UsersModel(object):

    @classmethod
    def build_user_id(username):
        """
        generate internal user id from username
        """
        return "user-{}".format(username)

    @classmethod
    def create_user(username, password):
        """
        create a new user, making sure it username is unique
        """
        user = redis.hget("user-{}".format(username), "user")
        if user is not None:
            raise BadRequest("User already exists")
        
        print("New User: {}".format(username), file=sys.stderr)
        hashed = Authorization.hash_password(password)
        user_dict = {
            'user' : username,
            'password_hash' : str(hashed)
        }

        user_id = UsersModel.build_user_id(username)
        print(user_id, file=sys.stderr)
        redis.hmset(user_id, user_dict)
        print(redis.hgetall(user_id), file=sys.stderr)
        return user_id

    @classmethod
    def login(username, password):
        """
        logs the given user in and returns a jwt token
        """
        user_id = UsersModel.build_user_id(username)
        hashed = redis.hget(user_id, 'password_hash')
        if hashed is None or not Authorization.check_password(password, hashed):
            raise Unauthorized("username or password is not correct")
    
        return Authorization.encode_jwt_token(user_id)

    @classmethod
    def logout(user, token):
        """
        logs the given user out and blocks the jwt token
        """
        Authorization.add_to_blocklist(token)
        return True

