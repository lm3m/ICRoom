from flask import Flask, Blueprint
from redis import RedisError
import os
import socket
from rest_plus import api
from controllers.user_controller import prefix as users_namespace
from controllers.topics_controller import prefix as topics_namespace
from controllers.messages_controller import prefix as messages_namespace
from database import redis

app = Flask(__name__)

def main():
    """
    setup the swagger and routes
    """
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(users_namespace)
    api.add_namespace(topics_namespace)
    api.add_namespace(messages_namespace)
    app.register_blueprint(blueprint)
    app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    main()

