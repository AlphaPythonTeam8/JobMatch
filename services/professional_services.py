from data import  schemas, models
from sqlalchemy.orm import Session


def register(user: schemas.ProfessionalRegistration, db: Session):
    db_user = models.Professional(Username=user.Username, FirstName=user.FirstName, LastName=user.LastName,
                                  Password=user.password)
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


def get_personal_info(id: int):
    pass


def create_ad(id: int):
    pass


def get_pro_by_username(db: Session, username: str):
    return db.query(models.Professional).filter(models.Professional.Username == username).first()