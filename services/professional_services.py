from data import schemas, models
from sqlalchemy.orm import Session
import sqlalchemy.exc
from data.schemas import CompanyAdResponse, CompanyAdsResponse, Professional, ProfessionalResponse


def register(user: schemas.ProfessionalRegistration, db: Session):
    db_user = models.Professional(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_ads(id: int, sort, db: Session):
    res = []
    if sort == 'asc':
        order_query = models.CompanyAd.UpdatedAt.asc()
    else:
        order_query = models.CompanyAd.UpdatedAt.desc()
    ads = db.query(models.CompanyAd).join(
        models.CompanyAdSkill, models.CompanyAd.CompanyAdID == models.CompanyAdSkill.CompanyAdID).join(
        models.Skill, models.CompanyAdSkill.SkillID == models.Skill.SkillID
    ).filter(models.CompanyAd.ProfessionalID == id).order_by(order_query)
    for ad in ads:
        skills = db.query(models.Skill.Description, models.CompanyAdSkill.Level).join(
            models.CompanyAdSkill, models.CompanyAdSkill.SkillID == models.Skill.SkillID).join(
            models.CompanyAd, models.CompanyAd.CompanyAdID == models.CompanyAdSkill.CompanyAdID).filter(
            models.CompanyAd.CompanyAdID == ad.CompanyAdID).all()
        res.append(CompanyAdsResponse(
            BottomSalary=ad.BottomSalary,
            TopSalary=ad.TopSalary,
            MotivationDescription=ad.MotivationDescription,
            Location=ad.Location,
            Skills=[' - '.join(skill) for skill in skills],
            Status=ad.Status,
            CompanyAdRequirement=ad.CompanyAdRequirement,
            CreatedAt=ad.CreatedAt,
            UpdatedAt=ad.UpdatedAt
        ))
    return res


def get_ad(id: int, db: Session):
    ad = db.query(models.CompanyAd).filter(models.CompanyAd.CompanyAdID == id).first()
    return ad


def return_ad(ad, db: Session):
    skills = db.query(models.Skill.Description, models.CompanyAdSkill.Level).join(
            models.CompanyAdSkill, models.CompanyAdSkill.SkillID == models.Skill.SkillID).join(
            models.CompanyAd, models.CompanyAd.CompanyAdID == models.CompanyAdSkill.CompanyAdID).filter(
            models.CompanyAd.CompanyAdID == ad.CompanyAdID).all()
    names = get_names(ad.ProfessionalID, db)
    return CompanyAdResponse(
        FirstName=names.FirstName,
        LastName=names.LastName,
        BottomSalary=ad.BottomSalary,
        TopSalary=ad.TopSalary,
        MotivationDescription=ad.MotivationDescription,
        Location=ad.Location,
        Skills=[' - '.join(skill) for skill in skills],
        Status=ad.Status,
        CreatedAt=ad.CreatedAt,
        UpdatedAt=ad.UpdatedAt,
        CompanyAdRequirement=ad.CompanyAdRequirement
        )

def edit_ad(new_ad, id: int, db: Session):
    skills = new_ad.Skills.split(', ')
    add_skills_to_db(skills, db)
    add_skills_to_ad(id, skills, db)
    ad_query = db.query(models.CompanyAd).filter(models.CompanyAd.CompanyAdID == id)
    ad_query.update(dict(BottomSalary=new_ad.BottomSalary, TopSalary=new_ad.TopSalary,
                         MotivationDescription=new_ad.MotivationDescription, Location=new_ad.Location,
                         Status=new_ad.Status), synchronize_session=False)
    db.commit()
    new_ad = ad_query.first()
    names = get_names(db.query(models.CompanyAd.ProfessionalID).filter(models.CompanyAd.CompanyAdID==id).first()[0], db)
    return CompanyAdResponse(
        FirstName=names.FirstName,
        LastName=names.LastName,
        BottomSalary=new_ad.BottomSalary,
        TopSalary=new_ad.TopSalary,
        MotivationDescription=new_ad.MotivationDescription,
        Location=new_ad.Location,
        Status=new_ad.Status,
        Skills= list(skills),
        CompanyAdRequirement=new_ad.CompanyAdRequirement,
        CreatedAt=new_ad.CreatedAt,
        UpdatedAt=new_ad.UpdatedAt
    )



def set_main_ad(id: int):
    pass


def create_ad(id: int, skills, ad: schemas.CompanyAd, db: Session):
    new_ad = models.CompanyAd(ProfessionalID=id, BottomSalary=ad.BottomSalary, TopSalary=ad.TopSalary,
                              MotivationDescription=ad.MotivationDescription, Location=ad.Location)
    db.add(new_ad)
    db.flush()
    db.commit()
    db.refresh(new_ad)
    add_skills_to_ad(new_ad.CompanyAdID, skills, db)
    ad = db.query(models.CompanyAd).filter(models.CompanyAd.CompanyAdID==new_ad.CompanyAdID).first()
    names = get_names(id, db)
    return CompanyAdResponse(
        FirstName=names.FirstName,
        LastName=names.LastName,
        BottomSalary=ad.BottomSalary,
        TopSalary=ad.TopSalary,
        MotivationDescription=ad.MotivationDescription,
        Location=ad.Location,
        Skills=skills,
        Status=ad.Status,
        CreatedAt=ad.CreatedAt,
        UpdatedAt=ad.UpdatedAt,
        CompanyAdRequirement=ad.CompanyAdRequirement
    )


def get_pro_by_username(db: Session, username: str):
    return db.query(models.Professional).filter(models.Professional.Username == username).first()


def get_pro(id: int, db: Session):
    profile = db.query(models.Professional).filter(models.Professional.ProfessionalID == id).first()
    count_ads = db.query(models.CompanyAd).filter(models.CompanyAd.ProfessionalID==id, models.CompanyAd.Status=="Active").count()
    return ProfessionalResponse(
        Username=profile.Username,
        FirstName=profile.FirstName,
        LastName=profile.LastName,
        ProfessionalEmail=profile.ProfessionalEmail,
        BriefSummary=profile.BriefSummary,
        Location=profile.Location,
        Status=profile.Status,
        Contact=profile.Contact,
        ActiveAds=count_ads
    )


def update_info(id: int, profile: schemas.ProfessionalUpdate, db: Session):
    profile_query = db.query(models.Professional).filter(models.Professional.ProfessionalID == id)
    profile_query.update(profile.model_dump(), synchronize_session=False)
    db.commit()
    profile = profile_query.first()
    count_ads = db.query(models.CompanyAd).filter(models.CompanyAd.ProfessionalID == id,
                                                  models.CompanyAd.Status == "Active").count()
    return ProfessionalResponse(
        Username=profile.Username,
        FirstName=profile.FirstName,
        LastName=profile.LastName,
        ProfessionalEmail=profile.ProfessionalEmail,
        BriefSummary=profile.BriefSummary,
        Location=profile.Location,
        Status=profile.Status,
        Contact=profile.Contact,
        ActiveAds=count_ads
    )


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
        try:
            skill, level = data.split(' - ')
            skill_id = db.query(models.Skill.SkillID).filter(models.Skill.Description == f"{skill}")
            db.add(models.CompanyAdSkill(CompanyAdID=ad, SkillID=skill_id, Level=level))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            continue


def get_names(id, db):
    return db.query(models.Professional.FirstName,
                     models.Professional.LastName).filter(models.Professional.ProfessionalID == id).first()
