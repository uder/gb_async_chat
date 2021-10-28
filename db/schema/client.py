from sqlalchemy import Column, String, Integer

from . import Base


class ClientTable(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    comment = Column(String(30), nullable=True)

    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return "<Client('%s','%s')>" % (self.name, self.comment)
