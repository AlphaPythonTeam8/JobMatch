from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus


load_dotenv()

#in the .env file there should be a variable JOB_MATCH_DB_PASSWORD=***** containing the DB password
db_password = os.getenv('JOB_MATCH_DB_PASSWORD')

encoded_password = quote_plus(db_password)

SQLALCHEMY_DATABASE_URL = f"mariadb+mariadbconnector://root:{encoded_password}@localhost/jobmatch"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
