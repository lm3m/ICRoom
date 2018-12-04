import sys
import logging
import uuid

from flask_restplus import fields
from rest_plus import api
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from models.topics_model import TopicsModel
from models.users_model import UsersModel
from datetime import datetime

log = logging.getLogger(__name__)

# model for user creation
messages_model = api.model('Topic', {
    'message_body': fields.String(required=True, description='Message Body'),
    'topic_id': fields.String(required=True, description='Parent Topic, cannot be null'),
    'parent_id': fields.String(required=False, description='Parent Message, can be null.')
})


class MessagesModel(object):
    @staticmethod
    def message_exists(message_id):
        message = redis.get(message_id)
        if message is not None:
            return True
        return False

    @staticmethod
    def create_message(creator_id, message_body, topic_id, parent_id=None):
        if not TopicsModel.topic_exists(topic_id):
            raise BadRequest("Topic does not exist, id={}".format(topic_id))

        if not UsersModel.user_exists(creator_id):
            raise BadRequest("User does not exist, id={}".format(creator_id))

        if parent_id is not None and not MessagesModel.message_exists(parent_id):
            raise BadRequest("Parent message does not exist, id={}".format(parent_id))

        message_time = datetime.utcnow()
        message_id = str(uuid.uuid4())
        message_dict = {
            "creator_id": creator_id,
            "topic_id": topic_id,
            "message_id": message_id,
            "creation_datetime_utc": str(message_time)
        }

        if parent_id is not None:
            message_dict['parent_id'] = parent_id

        redis.set(message_id, message_body)
        redis.hmset("message-{}".format(message_id), message_dict)
        redis.zadd("messages", {message_id: message_time.strftime("%s")})

        return message_id

    @staticmethod
    def list_messages():
        print(str(redis.zrevrange("messages", 0, 49, withscores=True)), file=sys.stderr)

        return redis.zrevrange("messages", 0, 49)

