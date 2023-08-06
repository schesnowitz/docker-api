from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = 'postgres'
password = 'pYXuIbSyXX2CFcHFKTkh'
host = 'containers-us-west-186.railway.app'
port = 7052
database = 'railway'

ALCHEMY_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(ALCHEMY_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
