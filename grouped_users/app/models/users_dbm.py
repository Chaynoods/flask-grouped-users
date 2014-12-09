from .user import User
from .membership import Membership
from .memberships_dbm import MembershipsDBM

class UsersDBM:
  def __init__(self, db):
    self.db = db

  def reset(self):
    self.db.drop_users()

  def all(self):
    users = [ User.from_json(user_json) for user_json in self.db.users ]
    membership_dbm = MembershipsDBM(self.db)
    for user in users:
      for membership in membership_dbm.find_by_userid(user.userid):
        user.group_names.append(membership.group_name)
    return users

  def find_by_id(self, user_id):
    matching_users = list(filter(lambda u: u.userid == user_id, self.all()))
    if len(matching_users) == 0:
      return None
    return matching_users[0]

  def create(self, json):
    user = User.from_json(json)
    self.db.users.append(user.to_db())
    if 'groups' in json:
      for group_name in json['groups']:
        membership = Membership(group_name, user.userid)
        self.db.memberships.append(membership.to_db())

  def update(self, json):
    self.delete(json['userid'])
    self.create(json)

  def delete(self, user_id):
    self.db.users = list(filter(lambda u: u['userid'] != user_id, self.db.users))
    MembershipsDBM(self.db).delete_matching_userid(user_id)
