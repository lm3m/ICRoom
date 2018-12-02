import sys
import logging

from flask_restplus import fields
from rest_plus import api
from database import redis
from werkzeug.exceptions import HTTPException, BadRequest, NotImplemented, Unauthorized
from auth import Authorization

log = logging.getLogger(__name__)

# model for user creation
topics_model = api.model('Topic', {
    'title': fields.String(required=True, description='Topic Title'),
    'description': fields.String(required=True, description='Topic Description')
})

class TopicsModel(object):
    @staticmethod
    def build_topic_name(title):
        return "topic-{}".format(title)

    @staticmethod
    def create_topic(title, description):
        """
        creates a new topic, validating that the topic title is unique
        :param title:
        :param description:
        :return topic id:
        """
        topic_label = TopicsModel.build_topic_name(title)
        print(topic_label, file=sys.stderr)

        topic_title = redis.hget(topic_id, "title")
        if topic_title is not None:
            raise BadRequest("Topic already exists")

        topic_id = redis.incr("topic_count")
        redis.lset("topic-list", topic_id, topic_label)

        topic_dict = {
            'title': title,
            'decription': description
        }

        redis.hmset(topic_label, topic_dict)
        print(redis.hgetall(topic_label), file=sys.stderr)
        return topic_id

    @staticmethod
    def list_topics():
        """
        gets the list of all topics
        :return all topics:
        """
        topic_list = []
        topic_array = redis.lrange("topic-list", 0, -1)
        for index, topic_label in enumerate(topic_array):
            topic = redis.hget(topic_label)
            topic['id'] = index
            topic_list.append(topic)

        return topic_list


