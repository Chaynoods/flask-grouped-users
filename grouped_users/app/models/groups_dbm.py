from .group import Group
from .membership import Membership
from .memberships_dbm import MembershipsDBM

class GroupsDBM:
  def __init__(self, db):
    self.db = db

  def reset(self):
    self.db.drop_groups()

  def all(self):
    groups = [ Group.from_json(group_json) for group_json in self.db.groups ]
    membership_dbm = MembershipsDBM(self.db)
    for group in groups:
      for membership in membership_dbm.find_by_group_name(group.name):
        group.userids.append(membership.userid)
    return groups

  def find_by_name(self, group_name):
    matching_groups = list(filter(lambda g: g.name == group_name, self.all()))
    if len(matching_groups) == 0:
      return None
    return matching_groups[0]

  def create(self, group_name):
    group = Group(group_name)
    self.db.groups.append(group.to_db())

  def update(self, group_name, userids):
    self.delete(group_name)
    group = Group(group_name, userids)
    self.db.groups.append(group.to_db())
    for userid in userids:
      membership = Membership(group_name, userid)
      self.db.memberships.append(membership.to_db())

  def delete(self, group_name):
    self.db.groups = list(filter(lambda g: g['name'] != group_name, self.db.groups))
    MembershipsDBM(self.db).delete_matching_group_name(group_name)