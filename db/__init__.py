import sqlalchemy

from schema import Base


engine = sqlalchemy.create_engine('sqlite://:memory:', echo=True)

Base.metadata.create_all(engine)
