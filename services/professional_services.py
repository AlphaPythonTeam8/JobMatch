from data import schemas, models
from sqlalchemy.orm import Session
import sqlalchemy.exc

from data.schemas import CompanyAdResponse


def register(user: schemas.ProfessionalRegistration, db: Session):
    db_user = models.Professional(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_ads(id: int, db: Session):
    pass


def get_ad(id: int):
    pass


def edit_ad(id: int):
    pass


def set_main_ad(id: int):
    pass


def create_ad(id: int, skills, ad: schemas.CompanyAd, db: Session):
    new_ad = models.CompanyAd(ProfessionalID=id, SalaryRange=ad.SalaryRange,
                              MotivationDescription=ad.MotivationDescription, Location=ad.Location)
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    add_skills_to_ad(new_ad.CompanyAdID, skills, db)
    names = db.query(models.Professional.FirstName,
                     models.Professional.LastName).filter(models.Professional.ProfessionalID == id).first()
    return CompanyAdResponse(
        FirstName=names.FirstName,
        LastName=names.LastName,
        SalaryRange=ad.SalaryRange,
        MotivationDescription=ad.MotivationDescription,
        Location=ad.Location,
        Skills=skills,
        Status=ad.Status
    )


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


def add_skills_to_db(skills, db: Session):
    for data in skills:
        skill, level = data.split(' - ')
        try:
            db.add(models.Skill(Description=skill))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            continue


def add_skills_to_ad(ad_id: int, skills, db: Session):
    ad = db.query(models.CompanyAd.CompanyAdID).filter(models.CompanyAd.CompanyAdID == ad_id)
    for data in skills:
        skill, level = data.split(' - ')
        skill_id = db.query(models.Skill.SkillID).filter(models.Skill.Description == f"{skill}")
        db.add(models.CompanyAdSkill(CompanyAdID=ad, SkillID=skill_id, Level=level))
        db.commit()
