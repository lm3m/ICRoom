import logging

from flask_restplus import Api

log = logging.getLogger(__name__)

api = Api(version='0.0', title='ICRoom', description='Chat Room for Iconic Exercise')

