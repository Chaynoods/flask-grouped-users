from .user import User
from .group import Group
from .membership import Membership

class MembershipsDBM:
  def __init__(self, db):
    self.db = db

  def reset(self):
    self.db.drop_memberships()

  def all(self):
    return [ Membership.from_json(membership_json) for membership_json in self.db.memberships ]

  def find_by_group_name(self, group_name):
    return list(filter(lambda g: g.group_name == group_name, self.all()))

  def find_by_userid(self, userid):
    return list(filter(lambda u: u.userid == userid, self.all()))

  def create(self, json):
    membership = Membership.from_json(json)
    self.db.memberships.append(membership.to_db())

  def delete_matching_group_name(self, group_name):
    self.db.memberships = list(filter(lambda g: g['group_name'] != group_name, self.db.memberships))

  def delete_matching_userid(self, userid):
    self.db.memberships = list(filter(lambda u: u['userid'] != userid, self.db.memberships))
