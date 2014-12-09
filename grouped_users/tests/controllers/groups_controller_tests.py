import json
from controller_test_case import ControllerTestCase

class GroupsControllerTestCase(ControllerTestCase):
  def default_user_json(self, userid='myuserid'):
    return {
      'first_name': 'Jane',
      'last_name':  'Doe',
      'userid': userid
    }

  def make_a_user(self, userid='myuserid'):
    return self.app.post('/users/{0}'.format(userid),
      data=json.dumps(self.default_user_json(userid)),
      content_type='application/json')

  def make_a_group(self, groupname='mygroupname'):
    return self.app.post('/groups/{0}'.format(groupname))

  def make_a_group_with_users(self, groupname='mygroupname', users=None):
    if users is None:
      userid = 'myuserid'
      self.make_a_user(userid)
      users = [userid]

    self.make_a_group(groupname)
    return self.app.put('/groups/{0}'.format(groupname),
      data=json.dumps(users),
      content_type='application/json')

  def test_get_group(self):
    groupname = 'mygroupname'
    userid = 'myuserid'
    self.make_a_user(userid)
    self.make_a_group_with_users(groupname, [userid])

    # get made group
    get_response = self.app.get('/groups/{0}'.format(groupname))
    self.check_response(get_response, 200,
      {'name': groupname, 'uri': 'http://localhost/groups/{0}'.format(groupname), 'userids': [userid]})

  def test_get_nonexistant_group(self):
    response = self.app.get('/groups/nonce')
    self.check_response(response, 404, 
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def test_get_empty_group(self):
    groupname = 'mygroupname'
    self.make_a_group(groupname)
    response = self.app.get('/groups/{0}'.format(groupname))
    self.check_response(response, 404, 
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def test_create_valid_empty_group(self):
    groupname = 'mygroupname'
    create_response = self.app.post('/groups/{0}'.format(groupname))
    self.check_response(create_response, 201,
      {'uri': 'http://localhost/groups/{0}'.format(groupname), 'name': groupname, 'userids': []})

  def test_create_duplicate_groupname(self):
    # Empty groups throw 409 on duplicate creation
    groupname = 'mygroupname'
    self.make_a_group(groupname)

    create_response = self.app.post('/groups/{0}'.format(groupname))
    self.check_response(create_response, 409,
      {'error': 'group with name mygroupname already exists'})

    self.db.reset()

    # Full groups also throw 409 on duplicate creation
    groupname = 'mygroupname'
    self.make_a_group_with_users(groupname)

    create_response = self.app.post('/groups/{0}'.format(groupname))
    self.check_response(create_response, 409,
      {'error': 'group with name mygroupname already exists'})

  def test_delete_empty_group(self):
    groupname = 'mygroupname'
    self.make_a_group(groupname)

    delete_response = self.app.delete('/groups/{0}'.format(groupname))
    self.check_response(delete_response, 404, 
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def test_delete_full_group(self):
    groupname = 'mygroupname'
    userid = 'myuserid'
    self.make_a_user(userid)
    self.make_a_group_with_users(groupname, [userid])

    # check that the user now has the group
    user_response = self.app.get('/users/{0}'.format(userid))
    assert json.loads(user_response.data)['groups'] == [groupname]

    # delete made group
    delete_response = self.app.delete('/groups/{0}'.format(groupname))
    self.check_response(delete_response, 200,
      {'uri': 'http://localhost/groups/{0}'.format(groupname), 'name': groupname, 'userids': [userid]})

    # check that get now fails
    response = self.app.get('/groups/{0}'.format(groupname))
    self.check_response(response, 404, 
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

    # check that the user now doesn't have the group
    user_response = self.app.get('/users/{0}'.format(userid))
    assert json.loads(user_response.data)['groups'] == []

  def test_delete_nonexistant_group(self):
    response = self.app.delete('/groups/nonce')
    self.check_response(response, 404, 
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def update_and_verify_group(self, groupname, new_userids):
    update_response = self.app.put('/groups/{0}'.format(groupname), data=json.dumps(new_userids), content_type='application/json')
    expected_response = {'userids': new_userids, 'name': groupname, 'uri': 'http://localhost/groups/{0}'.format(groupname)}
    self.check_response(update_response, 200, expected_response)

    # check that get now has the new data too
    get_response = self.app.get('/groups/{0}'.format(groupname))
    self.check_response(get_response, 200, expected_response)

    # and check that the users now have the group
    for userid in new_userids:
      user_response = self.app.get('/users/{0}'.format(userid))
      assert groupname in json.loads(user_response.data)['groups']

  def test_add_users_to_group(self):
    groupname = 'mygroupname'
    self.make_a_group(groupname)

    userid = 'myuserid'
    self.make_a_user(userid)
    userid2 = 'myuserid2'
    self.make_a_user(userid2)

    # add a user to the group
    self.update_and_verify_group(groupname, [userid])

    # add another user to the group
    self.update_and_verify_group(groupname, [userid, userid2])

  def test_remove_users_from_group(self):
    userid = 'myuserid'
    self.make_a_user(userid)
    userid2 = 'myuserid2'
    self.make_a_user(userid2)

    groupname = 'mygroupname'
    self.make_a_group_with_users(groupname, [userid, userid2])

    # remove a user from the group
    self.update_and_verify_group(groupname, [userid2])

    # remove all users from the group
    post_data = []
    update_response = self.app.put('/groups/{0}'.format(groupname), data=json.dumps(post_data), content_type='application/json')
    self.check_response(update_response, 200,
      {'userids': post_data, 'name': groupname, 'uri': 'http://localhost/groups/{0}'.format(groupname)})

    # check that get now returns 404
    get_response = self.app.get('/groups/{0}'.format(groupname))
    self.check_response(get_response, 404, 
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def test_add_nonexistant_user(self):
    groupname = 'mygroupname'
    self.make_a_group(groupname)

    nonce_userid = 'nonce'
    response = self.app.put('/groups/{0}'.format(groupname), data=json.dumps([nonce_userid]), content_type='application/json')
    self.check_response(response, 400,
      {'error': 'User with id {0} was not found'.format(nonce_userid)})

  def test_update_with_invalid_fields(self):
    groupname = 'mygroupname'
    self.make_a_group(groupname)

    # without post body data
    response = self.app.put('/groups/{0}'.format(groupname))
    self.check_response(response, 400,
      {'error': 'No array of userids to be placed in the group was provided'})

    # with post body data that is not just an array
    crazy_data = {'nonce': 'values'}
    response = self.app.put('/groups/{0}'.format(groupname), data=json.dumps(crazy_data), content_type='application/json')
    self.check_response(response, 400,
      {'error': 'No array of userids to be placed in the group was provided'})

  def test_update_nonexistant_group(self):
    # without post body data
    response = self.app.put('/groups/nonce')
    assert 400 == response.status_code

    # with post body data
    userid = 'myuserid'
    self.make_a_user(userid)
    response = self.app.put('/groups/nonce2',
      data=json.dumps([userid]),
      content_type='application/json')
    assert 404 == response.status_code

suite = GroupsControllerTestCase.suite()