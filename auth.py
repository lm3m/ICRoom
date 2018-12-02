import bcrypt
import jwt
import datetime
import sys

from functools import wraps
from database import redis
from redis import RedisError
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from config import config

def get_auth_token(headers):
    if not 'Authorization' in headers:
        raise Unauthorized("Authorization header required")
        
    data = headers['Authorization']
    print(str(data), file=sys.stderr)
    token = str.replace(str(data), 'Bearer ','')
    print(str(token), file=sys.stderr)
    return token

def validate_decode_token(token):
    try:
        if check_crl(token):
            raise Unauthorized("Authorization header revoked")
        print(str(token), file=sys.stderr)    
        payload = jwt.decode(token, 
                             config['DEFAULT']['SECRET_KEY'],
                             algorithms=['HS256'])
        user = payload['sub']

        return user
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        raise Unauthorized("Authorization header invalid")

def requires_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        token = get_auth_token(request.headers)
        user = validate_decode_token(token)
        return f(user, *args, **kws)            
    return decorated_function

def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def check_password(password, password_hash):
    return bcrypt.checkpw(password, password_hash)

def encode_jwt_token(user_id):
    """
    return encoded jwt token as a string
    """
    try: 
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        
        print(str(payload), file=sys.stderr)
        token = jwt.encode(
            payload,
            config['DEFAULT']['SECRET_KEY']).decode('utf-8')
        print(str(token), file=sys.stderr)
        return token
    except Exception as e:
        print(str(e), file=sys.stderr)
        raise e    

def add_to_crl(token):
    redis.sadd("CRL", token)

def check_crl(token):
    return redis.sismember("CRL", token)
