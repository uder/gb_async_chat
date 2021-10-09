from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from . import Base


class ClientHistoryTable(Base):
    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    login_at = Column(DateTime, default=func.now())
    login_ip = Column(Integer)

    def __init__(self, login, ip):
        self.login = login
        self.ip = ip

    def __repr__(self):
        return "<History('%s','%s')>" % (self.login, self.ip)

