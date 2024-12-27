from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

database_url = 'sqlite:///./database.txt'

engine = create_engine(database_url)

sessionLocal = sessionmaker(bind=engine)

base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
