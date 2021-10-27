from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    comment = Column(String(30), nullable=True)

    def __init__(self, name, comment=None):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return "<Client('%s','%s')>" % (self.name, self.comment)


class ClientHistory(Base):
    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    login_at = Column(DateTime, default=func.now())
    login_ip = Column(Integer)

    def __init__(self, login, ip):
        self.login = login
        self.ip = ip

    def __repr__(self):
        return "<History('%s','%s')>" % (self.login, self.ip)


class ContactList(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, owner_id, user_id):
        self.owner_id = owner_id
        self.user_id = user_id

    def __repr__(self):
        return "<History('%s','%s')>" % (self.owner_id, self.user_id)


сlass UserPassword(Base):
    __tablename__ = 'user_password'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    hash = Column(String)
    salt = Column(String)

    def __init__(self, user_name, hash, salt):
        self.user_id = user_name
        self.hash = hash
        self.salt = salt

    def __repr__(self):
        return "<Password('%s','%s', '%s')>" % (self.user_name, self.hash, self.salt)
