class User:
  def __init__(self, user_id, first_name, last_name, group_names=[]):
    self.userid = user_id
    self.first_name = first_name
    self.last_name = last_name
    self.group_names = group_names

  def to_json(self):
    return {
      'userid': self.userid,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'groups': self.group_names,
    }

  def to_db(self):
    return {
      'userid': self.userid,
      'first_name': self.first_name,
      'last_name': self.last_name
    }

  @classmethod
  def from_json(klass, json):
    groups = json['groups'] if 'groups' in json else []
    return User(json['userid'],
      json['first_name'],
      json['last_name'],
      groups)

  @classmethod
  def validate(klass, json):
    for field in ['first_name', 'last_name']:
      if not field in json:
        return (False, field)
    return (True, None)