from flask import Flask, jsonify, abort, make_response
from models.db import DB

my_app = Flask(__name__)
my_db = DB()

# set up routing & controllers
from controllers import users_controller, groups_controller
my_app.register_blueprint(users_controller.users_blueprint)
my_app.register_blueprint(groups_controller.groups_blueprint)

# set up error handling
def json_error_description(error):
  return make_response(jsonify({'error': error.description}), error.code)
for error in list(range(400, 420)) + list(range(500,506)):
    my_app.error_handler_spec[None][error] = json_error_description 