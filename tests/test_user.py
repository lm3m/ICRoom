import unittest
from unittest.mock import patch
from fakeredis import FakeStrictRedis


import ICRoom.models.users_model

ICRoom.models.users_model.redis = FakeStrictRedis(decode_responses=True)


class test_create_user(unittest.TestCase):
    def test_simple_create(self):
        self.assertIsNotNone(ICRoom.models.users_model.UsersModel.create_user("new_user", "password"))

if __name__ == '__main__':
    unittest.main()
