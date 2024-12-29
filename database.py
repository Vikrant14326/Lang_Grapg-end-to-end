from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DB_URL = "sqllite:///./sql_app.db"


#SQLALCHEMY_DB_URL = "mysql://root:root@localhost/first_db"

engine=create_engine(SQLALCHEMY_DB_URL,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()