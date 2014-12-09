class Group:
  def __init__(self, group_name, userids=[]):
    self.name = group_name
    self.userids = userids

  def to_json(self):
    return {
      'name': self.name,
      'userids': self.userids,
    }

  def to_db(self):
    return { 'name': self.name }

  @classmethod
  def from_json(klass, json):
    userids = json['userids'] if 'userids' in json else []
    return Group(json['name'], userids)