import os
import unittest
import json
from app import my_app, my_db

class ControllerTestCase(unittest.TestCase):
  def setUp(self):
    my_app.config['TESTING'] = True
    self.app = my_app.test_client()
    self.db = my_db

  def tearDown(self):
    self.db.reset()

  def check_response(self, response, expected_code, expected_json):
    assert response.status_code == expected_code
    if not expected_json is None:
      assert json.loads(response.data) == expected_json

  @classmethod
  def suite(klass):
    return unittest.TestLoader().loadTestsFromTestCase(klass)
