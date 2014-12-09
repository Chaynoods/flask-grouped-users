#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for, Blueprint
from app import my_db
from ..models.users_dbm import UsersDBM
from ..models.groups_dbm import GroupsDBM
from ..models.user import User

users_blueprint = Blueprint('users_blueprint', __name__)
users_dbm = UsersDBM(my_db)
groups_dbm = GroupsDBM(my_db)

@users_blueprint.route('/users/<user_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def route_user(user_id):
  if request.method == 'POST':
    return create_user(request, user_id)
  elif request.method == 'PUT':
    return update_user(request, user_id)
  elif request.method == 'DELETE':
    return delete_user(user_id)
  else:
    return read_user(user_id)

def read_user(user_id):
  user = get_user_or_404(user_id)
  return success_with_user(user)

def delete_user(user_id):
  user = get_user_or_404(user_id)
  users_dbm.delete(user_id)
  return success_with_user(user)

def update_user(request, user_id):
  def user_found_behavior(user):
    if user is None:
      abort(404)
  json = validate_inbound_user(request, user_id, user_found_behavior)

  users_dbm.update(json)
  return read_user(json['userid'])

def create_user(request, user_id):
  def user_found_behavior(user):
    if user is not None:
      abort(409, '{0} with id {1} already exists'.format('user', user_id))
  json = validate_inbound_user(request, user_id, user_found_behavior)

  users_dbm.create(json)
  user = users_dbm.find_by_id(json['userid'])
  return jsonify(format_for_response(user)), 201

def get_user_or_404(user_id):
  user = users_dbm.find_by_id(user_id)
  if user is None:
    abort(404)
  return user

def validate_inbound_user(request, user_id, user_found_behavior):
  json = standardize_user_ids_or_abort(request.get_json(), user_id)
  validation = User.validate(json)
  if not validation[0]:
    abort(400, 'Provided {0} object was missing the {1} field'.format('user', validation[1]))

  user_id = json['userid']
  user = users_dbm.find_by_id(user_id)
  user_found_behavior(user)

  if 'groups' in json:
    for groupname in json['groups']:
      if not groups_dbm.find_by_name(groupname):
        abort(400, 'Group with name \'{0}\' was not found'.format(groupname))

  return json

def standardize_user_ids_or_abort(json, user_id):
  if not json:
    abort(400, 'No user data was provided in your request')
  if 'userid' in json:
    if user_id != json['userid']:
      abort(400, 'Provided user object had a userid that did not match the provided route')
  elif user_id:
    json['userid'] = user_id
  return json

def success_with_user(user):
  return jsonify(format_for_response(user))

def format_for_response(user):
  return dict(user.to_json().items() + {'uri': url_for('.route_user', user_id=user.userid, _external=True)}.items())