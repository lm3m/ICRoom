import sys
import logging
import uuid

from datetime import datetime
from flask_restplus import fields
from api import api
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from logs import log_debug

log = logging.getLogger(__name__)

# model for user creation
topics_model = api.model('Topic', {
    'title': fields.String(required=True, description='Topic Title'),
    'description': fields.String(required=True, description='Topic Description')
})


class TopicsModel(object):
    @staticmethod
    def topic_exists(topic_title):
        """
        checks to see if a topic exists for a given title
        """
        topic_id = redis.get(topic_title)
        if topic_id is not None:
            return True
        return False

    @staticmethod
    def topic_exists_by_id(topic_id):
        """
        checks to see if a topic exists for a given id
        """
        topic_title = redis.hget(topic_id, 'title')
        if topic_title is not None:
            return True
        return False

    @staticmethod
    def update_topic_activity(topic_id, timestamp):
        redis.zadd("topics", {topic_id: timestamp})

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
        log_debug(log,{topic_id: topic_time.timestamp()})
        TopicsModel.update_topic_activity(topic_id, topic_time.timestamp())
        log_debug(log, redis.hgetall(topic_id))
        return topic_id

    @staticmethod
    def list_topics():
        """
        gets the list of the 50 most recent topics
        :return top 50 topics:
        """
        topic_list = []
        topic_array = redis.zrevrange("topics", 0, 49)
        log_debug(log, topic_array)
        for topic_id in topic_array:
            topic = {}
            topic_details = redis.hgetall(topic_id)
            log_debug(log, topic_details)
            topic["id"] = topic_details['topic_id']
            topic["title"] = topic_details['title']
            topic["description"] = topic_details['description']
            topic_list.append(topic)

        log_debug(log, topic_list)
        return topic_list


