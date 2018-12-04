import unittest
from unittest.mock import patch
from fakeredis import FakeStrictRedis


import models.users_model

models.users_model.redis = FakeStrictRedis(decode_responses=True)


class test_create_user(unittest.TestCase):
    def test_simple_create(self):
        self.assertIsNotNone(models.users_model.UsersModel.create_user("new_user", "password"))

if __name__ == '__main__':
    unittest.main()
