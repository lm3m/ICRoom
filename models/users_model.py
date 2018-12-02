import sys
import logging

from flask_restplus import fields
from rest_plus import api
from database import redis
from redis import RedisError
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from config import config
from auth import hash_password, check_password, encode_jwt_token, requires_authorization, add_to_crl

log = logging.getLogger(__name__)

# model for user creation
users_model = api.model('User', {
    'username': fields.String(required=True, description='Unique Username'), 
    'password': fields.String(required=True, description='Password')
})


def build_user_id(username):
    """
    generate internal user id from username
    """
    return "user-{}".format(username)

def create_user(username, password):
    """
    create a new user, making sure it username is unique
    """
    user = redis.hget("user-{}".format(username), "user")
    if user is not None:
        raise BadRequest("User already exists")
        
    print("New User: {}".format(username), file=sys.stderr)
    hashed = hash_password(password)
    user_dict = {
        'user' : username,
        'password_hash' : str(hashed)
    }

    user_id = build_user_id(username)
    print(user_id, file=sys.stderr)
    redis.hmset(user_id, user_dict)
    print(redis.hgetall(user_id), file=sys.stderr)
    return user_id

def login(username, password):
    """
    logs the given user in and returns a jwt token
    """
    user_id = build_user_id(username)
    hashed = redis.hget(user_id, 'password_hash')
    if hashed is None or not check_password(password, hashed):
        raise Unauthorized("username or password is not correct")
    
    return encode_jwt_token(user_id)

def logout(user, token):
    """
    logs the given user out and blocks the jwt token
    """
    add_to_crl(token)
    return True

