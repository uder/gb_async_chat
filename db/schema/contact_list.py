from sqlalchemy import Column, Integer

from . import Base


class ContactListTable(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, owner_id, user_id):
        self.owner_id = owner_id
        self.user_id = user_id

    def __repr__(self):
        return "<History('%s','%s')>" % (self.owner_id, self.user_id)
