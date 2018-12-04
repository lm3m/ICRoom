import unittest
from unittest.mock import patch
import time
from tests.fixup_fakeredis import fixed_fake_redis

import ICRoom.models.topics_model

ICRoom.models.topics_model.redis = fixed_fake_redis

class test_create_user(unittest.TestCase):
    def test_simple_create(self):
        self.assertIsNotNone(ICRoom.models.topics_model.TopicsModel.create_topic("title", "fake topic"))
        self.assertIsNotNone(ICRoom.models.topics_model.TopicsModel.list_topics())

    def test_count(self):
        count = 55
        for topic_count in range(0, count):
            # delay for a tenth of a second, tests can run fast enough to generate the same timestamp
            time.sleep(.1)
            self.assertIsNotNone(ICRoom.models.topics_model.TopicsModel.create_topic("{}".format(topic_count), "fake topic {}".format(topic_count)))

        topics = ICRoom.models.topics_model.TopicsModel.list_topics()
        self.assertIsNotNone(topics)
        self.assertEqual(50, len(topics))
        self.assertEqual(topics[0]['title'], str(count-1))
        self.assertEqual(topics[-1]['title'], str(count-50))

if __name__ == '__main__':
    unittest.main()
