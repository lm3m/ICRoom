import logging

from flask import request, make_response, jsonify
from flask_restplus import Resource, fields
from rest_plus import api
from models.messages_model import MessagesModel, messages_model
from auth import requires_authorization

log = logging.getLogger(__name__)

prefix = api.namespace('messages', description='Controller for Messages')


@prefix.route('/')
class MessagesController(Resource):
    @prefix.doc('Create a new message')
    @prefix.expect(messages_model, validate=True)
    @requires_authorization
    def post(self):
        """
        creates a new message
        """
        return MessagesModel.create_message(api.payload['username'], api.payload['password']), 200

    @prefix.doc('List messages')
    @requires_authorization
    def get(self):
        """
        returns the first 50 messages
        :return:
        """
        return MessagesModel.list_messages(), 200

