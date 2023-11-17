from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://root:0505@localhost/jobmatch"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
