from data import schemas, models
from sqlalchemy.orm import Session


def register(user: schemas.ProfessionalRegistration, db: Session):
    db_user = models.Professional(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_ads(id: int):
    pass


def get_ad(id: int):
    pass


def edit_ad(id: int):
    pass


def set_main_ad(id: int):
    pass


def create_ad(id: int):
    pass


def get_pro_by_username(db: Session, username: str):
    return db.query(models.Professional).filter(models.Professional.Username == username).first()


def get_pro_by_id(id: int, db: Session):
    profile = db.query(models.Professional).filter(models.Professional.ProfessionalID == id).first()
    return profile


def update_info(id: int, profile: schemas.Professional, db: Session):
    profile_query = db.query(models.Professional).filter(models.Professional.ProfessionalID == id)
    profile_query.update(profile.model_dump(), synchronize_session=False)
    db.commit()
    return profile_query.first()
