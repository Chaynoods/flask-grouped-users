#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for, Blueprint
from app import my_db
from ..models.groups_dbm import GroupsDBM
from ..models.users_dbm import UsersDBM
from ..models.group import Group

groups_blueprint = Blueprint('groups_blueprint', __name__)
groups_dbm = GroupsDBM(my_db)
users_dbm = UsersDBM(my_db)

@groups_blueprint.route('/groups/<group_name>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def route_group(group_name):
  if request.method == 'POST':
    return create_group(request, group_name)
  elif request.method == 'PUT':
    return update_group(request, group_name)
  elif request.method == 'DELETE':
    return delete_group(request, group_name)
  else:
    return read_group(group_name)

def read_group(group_name):
  group = get_group_or_404(group_name)
  return success_with_group(group)

def delete_group(request, group_name):
  group = get_group_or_404(group_name)
  groups_dbm.delete(group_name)
  return success_with_group(group)

def update_group(request, group_name):
  userids = request.get_json()
  if userids is None or not isinstance(userids, list):
    abort(400, 'No array of userids to be placed in the group was provided')

  get_group_or_404(group_name, False)

  for userid in userids:
    if not users_dbm.find_by_id(userid):
      abort(400, 'User with id {0} was not found'.format(userid))

  groups_dbm.update(group_name, request.get_json())
  group = get_group_or_404(group_name, False)
  return success_with_group(group)

def create_group(request, group_name):
  group = groups_dbm.find_by_name(group_name)
  if group is not None:
    abort(409, '{0} with name {1} already exists'.format('group', group_name))

  groups_dbm.create(group_name)
  group = groups_dbm.find_by_name(group_name)
  return jsonify(format_for_response(group)), 201

def get_group_or_404(group_name, throw_on_empty=True):
  group = groups_dbm.find_by_name(group_name)
  if (group is None) or (throw_on_empty and len(group.userids) == 0):
    abort(404)
  return group

def success_with_group(group):
  return jsonify(format_for_response(group))

def format_for_response(group):
  return dict(group.to_json().items() + {'uri': url_for('.route_group', group_name=group.name, _external=True)}.items())