from http.client import HTTPException
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session
from data import schemas, models
from data.schemas import JobAdResponse
from services.company_services import get_company_name_by_id
from services.professional_services import add_skills_to_db, add_skills_to_ad
from sqlalchemy.orm import Session
from data.models import JobAd
from sqlalchemy.exc import IntegrityError
import sqlalchemy.exc


def get_all_job_ads_query(company_id: int, sort: str, db: Session):
    query = db.query(JobAd)
    if sort == 'asc':
        query = query.order_by(JobAd.UpdatedAt.asc())
    else:
        query = query.order_by(JobAd.UpdatedAt.desc())
    query = query.filter(JobAd.CompanyID == company_id)
    return query


def create_job_ad(id: int, skills, ad: schemas.JobAd, db: Session):
    new_ad = models.JobAd(CompanyID=id,
                          BottomSalary=ad.BottomSalary,
                          TopSalary=ad.TopSalary,
                          JobDescription=ad.JobDescription,
                          Location=ad.Location)
    db.add(new_ad)
    db.flush()
    db.commit()
    db.refresh(new_ad)
    add_skills_to_job_ad(new_ad.JobAdID, skills, db)
    ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == new_ad.JobAdID).first()
    names = get_names(id, db)
    return JobAdResponse(
        # Username=names.Username,
        # CompanyName=names.CompanyName,
        BottomSalary=ad.BottomSalary,
        TopSalary=ad.TopSalary,
        JobDescription=ad.JobDescription,
        Location=ad.Location,
        Status=ad.Status,
        Skills=skills,
        CreatedAt=ad.CreatedAt,
        UpdatedAt=ad.UpdatedAt
    )


def get_names(id, db):
    return db.query(models.Company.Username,
                    models.Company.CompanyName).filter(models.Company.CompanyID == id).first()


def add_skills_to_job_ad(ad_id: int, skills, db: Session):
    db.query(models.JobAdSkill).filter(models.JobAdSkill.JobAdID == ad_id).delete()
    for data in skills:
        try:
            skill, level = data.split(' - ')
            skill_id = db.query(models.Skill.SkillID).filter(models.Skill.Description == f"{skill}")
            db.add(models.JobAdSkill(JobAdID=ad_id, SkillID=skill_id, Level=level))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            continue


def get_all_job_ads(company_id: int, sort: str, db: Session):
    res = []
    if sort == 'asc':
        order_query = models.JobAd.UpdatedAt.asc()
    else:
        order_query = models.JobAd.UpdatedAt.desc()

    ads = db.query(models.JobAd).filter(
        models.JobAd.CompanyID == company_id).order_by(order_query)

    for ad in ads:
        skills = get_skills_for_job_ad(db, ad)
        # Filter out None values from skills and join the remaining elements
        skill_strings = [' - '.join(filter(None, skill)) for skill in skills]
        res.append(schemas.JobAdResponse2(
            JobAdID=ad.JobAdID,
            BottomSalary=ad.BottomSalary,
            TopSalary=ad.TopSalary,
            JobDescription=ad.JobDescription,
            Location=ad.Location,
            Status=ad.Status,
            Skills=skill_strings,
            CreatedAt=ad.CreatedAt,
            UpdatedAt=ad.UpdatedAt
        ))
    return res


def edit_job_ad(new_ad, id: int, db: Session):
    skills = new_ad.Skills.split(', ')
    add_skills_to_db(skills, db)
    add_skills_to_job_ad(id, skills, db)
    ad_query = db.query(models.JobAd).filter(models.JobAd.JobAdID == id)
    ad_query.update(dict(BottomSalary=new_ad.BottomSalary,
                         TopSalary=new_ad.TopSalary,
                         JobDescription=new_ad.JobDescription,
                         Location=new_ad.Location,
                         Status=new_ad.Status), synchronize_session=False)
    db.commit()
    new_ad = ad_query.first()
    # names = get_names(new_ad.ProfessionalID, db)
    return JobAdResponse(
        BottomSalary=new_ad.BottomSalary,
        TopSalary=new_ad.TopSalary,
        JobDescription=new_ad.JobDescription,
        Location=new_ad.Location,
        Status=new_ad.Status,
        Skills=list(skills),
        CreatedAt=new_ad.CreatedAt,
        UpdatedAt=new_ad.UpdatedAt
    )


def get_job_ad(job_ad_id: int, db: Session):
    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == job_ad_id).first()
    return job_ad


def return_job_ad(ad, db: Session):
    skills = get_skills_for_job_ad(db, ad)

    skills_str = [' - '.join(skill) if skill is not None else '' for skill in skills]
    return schemas.JobAdResponse2(
        JobAdID=ad.JobAdID,
        BottomSalary=ad.BottomSalary,
        TopSalary=ad.TopSalary,
        JobDescription=ad.JobDescription,
        Location=ad.Location,
        Status=ad.Status,
        Skills=skills_str,
        CreatedAt=ad.CreatedAt,
        UpdatedAt=ad.UpdatedAt
    )


def get_skills_for_job_ad(db, ad):
    return db.query(models.Skill.Description, models.JobAdSkill.Level).join(
        models.JobAdSkill, models.JobAdSkill.SkillID == models.Skill.SkillID).join(
        models.JobAd, models.JobAd.JobAdID == models.JobAdSkill.JobAdID).filter(
        models.JobAd.JobAdID == ad.JobAdID).all()
