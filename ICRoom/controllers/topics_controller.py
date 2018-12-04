import logging

from flask import request, make_response, jsonify
from flask_restplus import Resource, fields
from api import api
from models.topics_model import TopicsModel, topics_model
from auth import requires_authorization

log = logging.getLogger(__name__)

prefix = api.namespace('topics', description='Controller for Topics')

@prefix.route('/')
class TopicsController(Resource):
    @prefix.doc('Create a new topic')
    @prefix.expect(topics_model, validate=True)
    @requires_authorization
    def post(self, user):
        """
        creates a new topic
        """
        return TopicsModel.create_topic(api.payload['title'], api.payload['description']), 200

    @prefix.doc('View all topics')
    @requires_authorization
    def get(self, user):
        """
        get the list of topics
        :return list of all topics:
        """
        return TopicsModel.list_topics(), 200

