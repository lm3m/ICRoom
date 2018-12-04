import bcrypt
import jwt
import datetime
import sys
import logging

from flask import request
from functools import wraps
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from config import config
from logs import log_debug

log = logging.getLogger(__name__)

def requires_authorization(f):
    """
    decorator for token validation for routes
    """
    @wraps(f)
    def decorated_function(*args, **kws):
        token = Authorization.get_auth_token(request.headers)
        user = Authorization.validate_decode_token(token)
        return f(user, *args, **kws)

    return decorated_function


class Authorization(object):
    @staticmethod
    def get_auth_token(headers):
        """
        looks for Authorization header and returns the token if found
        :param headers:
        :return token:
        """
        if not 'Authorization' in headers:
            raise Unauthorized("Authorization header required")
        
        data = headers['Authorization']
        log_debug(log, str(data))
        token = str.replace(str(data), 'Bearer ','')
        log_debug(log, str(token))
        return token

    @staticmethod
    def validate_decode_token(token):
        """
        given a token validates that it is valid and not revoked
        :param token:
        :return user id for user from a valid token:
        """
        try:
            if Authorization.check_blocklist(token):
                raise Unauthorized("Authorization header revoked")
            log_debug(log, str(token))
            payload = jwt.decode(token,
                                 config['DEFAULT']['SECRET_KEY'],
                                 algorithms=['HS256'])
            user = payload['sub']

            return user
        except Exception as ex:
            log_debug(log, str(ex))
            raise Unauthorized("Authorization header invalid")

    @staticmethod
    def hash_password(password):
        """
        returns the hash for a given password
        :param password:
        :return hash:
        """
        return bcrypt.hashpw(password, bcrypt.gensalt())


    @staticmethod
    def check_password(password, password_hash):
        """
        validates a given password and hash match
        :param password:
        :param password_hash:
        :return if the hash matches, true or false:
        """
        return bcrypt.checkpw(password, password_hash)

    @staticmethod
    def encode_jwt_token(user_id):
        """
        return encoded jwt token as a string
        :param user_id:
        :return jwt token:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
        
            log_debug(log, str(payload))
            token = jwt.encode(
                payload,
                config['DEFAULT']['SECRET_KEY']).decode('utf-8')
            log_debug(log, str(token))
            return token
        except Exception as e:
            log_debug(log, str(e))
            raise e

    @staticmethod
    def add_to_blocklist(token):
        """
        adds a given token to the blocklist
        :param token:
        :return None:
        """
        redis.sadd("blocklist", token)

    @staticmethod
    def check_blocklist(token):
        """
        checks if a token has been added to the blocklist or not
        :param token:
        :return if the token is in blocklist, true or false:
        """
        return redis.sismember("blocklist", token)
