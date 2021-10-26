import sqlalchemy
from sqlalchemy.orm import sessionmaker

# from .schema import Base, ClientTable, ClientHistoryTable, ContactListTable
from .schema import Base

# engine = sqlalchemy.create_engine('sqlite://:memory:', echo=True)
engine = sqlalchemy.create_engine('sqlite:///db.sqlite', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
