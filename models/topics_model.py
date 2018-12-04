import sys
import logging

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
    def build_topic_name(title):
        return "topic-{}".format(title)

    @staticmethod
    def topic_exists(topic_id):
        topic_title = redis.hget(topic_id, "title")
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
        topic_label = TopicsModel.build_topic_name(title)
        print(topic_label, file=sys.stderr)

        topic_title = redis.hget(topic_label, "title")
        if TopicsModel.topic_exists(topic_label):
            raise BadRequest("Topic already exists")

        topic_id = redis.rpush("topic-list", topic_label)

        topic_dict = {
            'title': title,
            'description': description
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
            topic = {}
            topic_details = redis.hgetall(topic_label)
            print(topic_details, file=sys.stderr)
            topic["id"] = index
            topic["title"] = topic_details['title']
            topic["description"] = topic_details['description']
            topic_list.append(topic)

        print(topic_list, file=sys.stderr)
        return topic_list


