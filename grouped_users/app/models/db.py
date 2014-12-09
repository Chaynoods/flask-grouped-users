class DB:
  def __init__(self):
    self.users =[]
    self.groups =[]
    self.memberships =[]

  def drop_users(self):
    self.users = []
    self.memberships = []

  def drop_groups(self):
    self.groups = []
    self.memberships = []

  def drop_memberships(self):
    self.memberships = []

  def reset(self):
    self.drop_users()
    self.drop_groups()
    self.drop_memberships()
