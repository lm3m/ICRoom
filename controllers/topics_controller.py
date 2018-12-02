import logging

from flask_restplus import Resource, fields
from rest_plus import api
from models.topics_model import TopicsModel
from auth import requires_authorization

log = logging.getLogger(__name__)

prefix = api.namespace('topics', description='Controller for Topics')

@prefix.route('/')
class TopicsController(Resource):
    @requires_authorization
    @prefix.doc('Create a new topic')
    @prefix.expect(topic_model, validate=True)
    def post(self):
        """
        creates a new topic
        """
        return TopicsModel.create_topic(api.payload['title'], api.payload['description']), 200

    def get(self):
        """
        get the list of topics
        :return list of all topics:
        """
        return TopicsModel.list_topics(), 200

