from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus


load_dotenv()

db_host = os.getenv('JOB_MATCH_DB_HOST')
db_name = os.getenv('JOB_MATCH_DB_NAME')
db_user = os.getenv('JOB_MATCH_DB_USER')
db_password = os.getenv('JOB_MATCH_DB_PASSWORD')


#in the .env file there should be a variable JOB_MATCH_DB_PASSWORD=***** containing the DB password
db_password = os.getenv('JOB_MATCH_DB_PASSWORD')

encoded_password = quote_plus(db_password)

SQLALCHEMY_DATABASE_URL = f"mariadb+mariadbconnector://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
