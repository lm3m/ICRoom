import unittest
from unittest.mock import patch
import time
from tests.fixup_fakeredis import fixed_fake_redis

import models.messages_model
import models.users_model
import models.topics_model

models.messages_model.redis = fixed_fake_redis

def always_true(object):
    return True

def always_false(object):
    return False


class test_create_message(unittest.TestCase):
    @patch('models.messages_model.UsersModel.user_exists')
    @patch('models.messages_model.TopicsModel.topic_exists_by_id')
    @patch('models.messages_model.MessagesModel.message_exists')
    def test_simple_create(self, user_mock, topic_mock, message_mock):
        user_mock.return_value = True
        topic_mock.return_value = True
        message_mock.return_value = True

        self.assertIsNotNone(models.messages_model.MessagesModel.create_message("creator_id", "message", "topic_id",))
        self.assertIsNotNone(models.messages_model.MessagesModel.list_messages())

    @patch('models.messages_model.UsersModel.user_exists')
    @patch('models.messages_model.TopicsModel.topic_exists_by_id')
    @patch('models.messages_model.MessagesModel.message_exists')
    def test_count(self, user_mock, topic_mock, message_mock):
        user_mock.return_value = True
        topic_mock.return_value = True
        message_mock.return_value = True

        count = 57
        for message_count in range(0, count):
            # delay for a tenth of a second, tests can run fast enough to generate the same timestamp
            time.sleep(.1)
            self.assertIsNotNone(models.messages_model.MessagesModel.create_message("creator_id", "{}".format(message_count), "topic_id"))

        messages = models.messages_model.MessagesModel.list_messages()
        self.assertIsNotNone(messages)
        self.assertEqual(50, len(messages))
        self.assertEqual(messages[0]['message_body'], str(count-1))
        self.assertEqual(messages[-1]['message_body'], str(count-50))


if __name__ == '__main__':
    unittest.main()

