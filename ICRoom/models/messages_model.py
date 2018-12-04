import logging
import uuid

from flask_restplus import fields
from api import api
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from models.topics_model import TopicsModel
from models.users_model import UsersModel
from datetime import datetime
from logs import log_debug

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
        """
        checks to see if a message exists for a given id
        """
        message = redis.get(message_id)
        if message is not None:
            return True
        return False

    @staticmethod
    def create_message(creator_id, message_body, topic_id, parent_id=None):
        """
        validates the input and then creates a message
        """
        if not TopicsModel.topic_exists_by_id(topic_id):
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
        """
        returns the most recent 50 messages created
        """
        message_list = []
        message_array = redis.zrevrange("messages", 0, 49)
        log_debug(message_array)
        for message_id in message_array:
            message = {}
            message_details = redis.hgetall("message-{}".format(message_id))
            log_debug(message_details)
            message['id'] = message_details['message_id']
            message['topic_id'] = message_details['topic_id']
            message['creator_id'] = message_details['creator_id']
            if 'parent_id' in message_details:
                message['parent_id'] = message_details['parent_id']
            message['message_body'] = redis.get(message_id)
            message_list.append(message)
        
        log_debug(message_list)
        return message_list
            

