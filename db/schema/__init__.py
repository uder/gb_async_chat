from sqlalchemy.orm import declarative_base

from client import ClientTable
from client_history import ClientHistoryTable
from contact_list import ContactListTable

Base = declarative_base()
