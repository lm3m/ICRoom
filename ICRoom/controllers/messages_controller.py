import sys
import logging

from flask import request, make_response, jsonify
from flask_restplus import Resource, fields
from api import api
from models.messages_model import MessagesModel, messages_model
from auth import requires_authorization
from logs import log_debug

log = logging.getLogger(__name__)

prefix = api.namespace('messages', description='Controller for Messages')


@prefix.route('/')
class MessagesController(Resource):
    @prefix.doc('Create a new message')
    @prefix.expect(messages_model, validate=True)
    @requires_authorization
    def post(user, self):
        """
        creates a new message
        """
        log_debug(log, user)
        message_body = api.payload['message_body']
        topic_id = api.payload['topic_id']
        parent_id = None
        if 'parent_id' in api.payload:
            parent_id = api.payload['parent_id']
        return MessagesModel.create_message(user, message_body, topic_id, parent_id), 200

    @prefix.doc('List messages')
    @requires_authorization
    def get(self, user):
        """
        returns the first 50 messages
        :return:
        """
        return MessagesModel.list_messages(), 200

