#!venv/bin/python
import unittest
from tests.controllers import users_controller_tests
from tests.controllers import groups_controller_tests

runner = unittest.TextTestRunner()
controllers_test_suite = unittest.TestSuite([
  users_controller_tests.suite,
  groups_controller_tests.suite
])
runner.run(controllers_test_suite)
