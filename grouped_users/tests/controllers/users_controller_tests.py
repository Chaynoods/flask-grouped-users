import json
from controller_test_case import ControllerTestCase

class UsersControllerTestCase(ControllerTestCase):
  def default_user_json(self, userid='myuserid'):
    return {
      'first_name': 'Jane',
      'last_name':  'Doe',
      'userid': userid,
      'groups': []
    }

  def make_a_user(self, userid='myuserid'):
    return self.app.post('/users/{0}'.format(userid),
      data=json.dumps(self.default_user_json(userid)),
      content_type='application/json')

  def test_get_user(self):
    userid = 'myuserid'
    post_data = self.default_user_json(userid)
    self.make_a_user(userid)

    # get made user
    get_response = self.app.get('/users/{0}'.format(userid))
    self.check_response(get_response, 200,
      dict(post_data.items() + {'uri': 'http://localhost/users/{0}'.format(userid)}.items()))

  def test_get_nonexistant_user(self):
    response = self.app.get('/users/nonce')
    self.check_response(response, 404,
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def test_create_valid_user(self):
    userid = 'myuserid'
    post_data = self.default_user_json(userid)
    create_response = self.app.post('/users/{0}'.format(userid), data=json.dumps(post_data), content_type='application/json')
    self.check_response(create_response, 201,
      dict(post_data.items() + {'uri': 'http://localhost/users/{0}'.format(userid)}.items()))

  def test_create_invalid_user(self):
    # missing last name
    post_data = dict(
      first_name='Jane',
      userid='myuserid',
      groups=[]
    )
    create_response = self.app.post('/users/myuserid', data=json.dumps(post_data), content_type='application/json')
    self.check_response(create_response, 400,
      {'error': 'Provided user object was missing the last_name field'})

    # non-existant group
    post_data = dict(
      first_name='Jane',
      last_name='Doe',
      userid='myuserid',
      groups=['nonce']
    )
    create_response = self.app.post('/users/myuserid', data=json.dumps(post_data), content_type='application/json')
    self.check_response(create_response, 400,
      {'error': "Group with name 'nonce' was not found"})

  def test_create_best_effort_userid(self):
    post_data_no_id = dict(
      first_name='Jane',
      last_name='Doe',
      groups=[]
    )
    create_response = self.app.post('/users/myuserid', data=json.dumps(post_data_no_id), content_type='application/json')
    self.check_response(create_response, 201,
      dict(post_data_no_id.items() + {'uri': 'http://localhost/users/myuserid', 'userid': 'myuserid'}.items()))

    post_data_wrong_id = dict(
      first_name='Jane',
      last_name='Doe',
      userid='nonce',
      groups=[]
    )
    create_response = self.app.post('/users/myuserid2', data=json.dumps(post_data_wrong_id), content_type='application/json')
    self.check_response(create_response, 400,
      {'error': 'Provided user object had a userid that did not match the provided route'})

  def test_create_duplicate_userid(self):
    userid = 'myuserid'
    self.make_a_user(userid)

    post_data = self.default_user_json(userid)
    create_response = self.app.post('/users/{0}'.format(userid), data=json.dumps(post_data), content_type='application/json')
    self.check_response(create_response, 409,
      {'error': 'user with id myuserid already exists'})

  def test_delete_user(self):
    userid = 'myuserid'
    post_data = self.default_user_json(userid)
    self.make_a_user(userid)

    # delete made user
    delete_response = self.app.delete('/users/{0}'.format(userid))
    self.check_response(delete_response, 200,
      dict(post_data.items() + {'uri': 'http://localhost/users/{0}'.format(userid)}.items()))

    # check that get now fails
    response = self.app.get('/users/{0}'.format(userid))
    self.check_response(response, 404,
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def test_delete_nonexistant_user(self):
    response = self.app.delete('/users/nonce')
    self.check_response(response, 404,
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

  def test_update_user(self):
    userid = 'myuserid'
    post_data = self.default_user_json(userid)
    self.make_a_user(userid)

    # modify the user
    post_data['first_name'] = 'John'
    update_response = self.app.put('/users/{0}'.format(userid), data=json.dumps(post_data), content_type='application/json')
    expected_response = dict(post_data.items() + {'uri': 'http://localhost/users/{0}'.format(userid)}.items())
    self.check_response(update_response, 200, expected_response)

    # check that get now has the new data too
    get_response = self.app.get('/users/{0}'.format(userid))
    self.check_response(update_response, 200, expected_response)

  def test_update_invalid_user(self):
    userid = 'myuserid'
    post_data = self.default_user_json(userid)
    self.make_a_user(userid)

    # modify the user in an invalid way (missing first name)
    del post_data['first_name']
    update_response = self.app.put('/users/{0}'.format(userid), data=json.dumps(post_data), content_type='application/json')
    self.check_response(update_response, 400,
      {'error': 'Provided user object was missing the first_name field'})

    # check that get still has the old data
    post_data = self.default_user_json(userid)
    get_response = self.app.get('/users/{0}'.format(userid))
    self.check_response(get_response, 200,
      dict(post_data.items() + {'uri': 'http://localhost/users/{0}'.format(userid)}.items()))

    # modify the user in an invalid way (non-existant group)
    post_data = self.default_user_json(userid)
    post_data['groups'] = ['nonce']
    update_response = self.app.put('/users/{0}'.format(userid), data=json.dumps(post_data), content_type='application/json')
    self.check_response(update_response, 400,
      {'error': "Group with name 'nonce' was not found"})

    # check that get still has the old data
    post_data = self.default_user_json(userid)
    get_response = self.app.get('/users/{0}'.format(userid))
    self.check_response(get_response, 200,
      dict(post_data.items() + {'uri': 'http://localhost/users/{0}'.format(userid)}.items()))

  def test_update_nonexistant_user(self):
    # without post body data
    response = self.app.put('/users/nonce')
    self.check_response(response, 400,
      {'error': 'No user data was provided in your request'})

    # with post body data
    userid = 'nonce2'
    post_data = self.default_user_json(userid)
    response = self.app.put('/users/{0}'.format(userid), data=json.dumps(post_data), content_type='application/json')
    self.check_response(response, 404,
      {'error': 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'})

suite = UsersControllerTestCase.suite()