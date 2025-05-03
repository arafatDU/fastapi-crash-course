from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABSE = 'postgresql://postgres:password@localhost:5432/QuizAppFastAPI'

engine = create_engine(URL_DATABSE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()