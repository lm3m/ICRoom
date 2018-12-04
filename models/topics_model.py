import sys
import logging
import uuid

from datetime import datetime
from flask_restplus import fields
from rest_plus import api
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized

log = logging.getLogger(__name__)

# model for user creation
topics_model = api.model('Topic', {
    'title': fields.String(required=True, description='Topic Title'),
    'description': fields.String(required=True, description='Topic Description')
})


class TopicsModel(object):
    @staticmethod
    def topic_exists(topic_title):
        topic_id = redis.get(topic_title)
        if topic_id is not None:
            return True
        return False

    @staticmethod
    def topic_exists_by_id(topic_id):
        topic_title = redis.hget(topic_id, 'title')
        if topic_title is not None:
            return True
        return False

    @staticmethod
    def create_topic(title, description):
        """
        creates a new topic, validating that the topic title is unique
        :param title:
        :param description:
        :return topic id:
        """
        if TopicsModel.topic_exists(title):
            raise BadRequest("Topic already exists")

        topic_time = datetime.utcnow()
        topic_id = str(uuid.uuid4())
        redis.set(title, topic_id)

        topic_dict = {
            'title': title,
            'description': description,
            'topic_id': topic_id,
            'creation_datetime_utc': str(topic_time)
        }

        redis.hmset(topic_id, topic_dict)
        redis.zadd("topics", {topic_id: topic_time.strftime("%s")})
        print(redis.hgetall(topic_id), file=sys.stderr)
        return topic_id

    @staticmethod
    def list_topics():
        """
        gets the list of all topics
        :return all topics:
        """
        topic_list = []
        topic_array = redis.zrevrange("topics", 0, 49)
        print(topic_array, file=sys.stderr)
        for topic_id in topic_array:
            topic = {}
            topic_details = redis.hgetall(topic_id)
            print(topic_details, file=sys.stderr)
            topic["id"] = topic_details['topic_id']
            topic["title"] = topic_details['title']
            topic["description"] = topic_details['description']
            topic_list.append(topic)

        print(topic_list, file=sys.stderr)
        return topic_list


