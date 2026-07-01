import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

engine = sa.create_engine("sqlite:///doacoes.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
