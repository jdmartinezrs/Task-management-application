from sqlalchemy import create_engine
from sqlalchemy.ext.declarative
import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///task.db"
engine = create_engine(DATABASE_URL,echo=True)
session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
