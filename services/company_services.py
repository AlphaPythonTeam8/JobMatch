from common.hashing import bcrypt_context
from data import schemas, models
from sqlalchemy.orm import Session


def register(user: schemas.CompanyRegistration, db: Session):
    hashed_password = bcrypt_context.hash(user.Password)
    user.Password = hashed_password

    db_user = models.Company(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_info(id: int):
    pass


def edit_info(id: int):
    pass


def create_ad(id: int):
    pass


def get_ad(company_id: int, ad_id: int):
    pass


def edit_ad(company_id: int, ad_id: int):
    pass


def get_company_by_username(db: Session, username: str):
    return db.query(models.Company).filter(models.Company.Username == username).first()


def get_company_by_id(id: int, db: Session):
    company_profile = db.query(models.Company).filter(models.Company.CompanyID == id).first()
    return company_profile


def update_info(id: int, profile: schemas.Company, db: Session):
    profile_query = db.query(models.Company).filter(models.Company.CompanyID == id)
    profile_query.update(profile.model_dump(), synchronize_session=False)
    db.commit()
    return profile_query.first()
