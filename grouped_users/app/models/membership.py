class Membership:
  def __init__(self, group_name, userid):
    self.group_name = group_name
    self.userid = userid

  def to_json(self):
    return {
      'group_name': self.group_name,
      'userid': self.userid,
    }

  def to_db(self):
    return self.to_json()

  @classmethod
  def from_json(klass, json):
    return Membership(json['group_name'], json['userid'])