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
def get_all_job_ads_query(company_id: int, sort: str, db: Session):
    query = db.query(JobAd)
    if sort == 'asc':
        query = query.order_by(JobAd.UpdatedAt.asc())
    else:
        query = query.order_by(JobAd.UpdatedAt.desc())
    query = query.filter(JobAd.CompanyID == company_id)
    return query


# def create_job_ad(company_id: int, skills, ad: schemas.JobAd, db: Session):
#     new_job_ad = models.JobAd(CompanyID=company_id, SalaryRange=ad.SalaryRange,
#                               JobDescription=ad.JobDescription, Location=ad.Location, JobRequirement=ad.JobRequirement)
#     db.add(new_job_ad)
#     db.commit()
#     db.refresh(new_job_ad)

#     add_skills_to_job_ad(new_job_ad.JobAdID, skills, db)
#     return new_job_ad
# def create_job_ad(id: int, skills, ad: schemas.JobAd, db: Session):
#     existing_ad = db.query(models.JobAd).filter(
#         models.JobAd.CompanyID == id,
#         models.JobAd.BottomSalary == ad.BottomSalary,
#         models.JobAd.TopSalary == ad.TopSalary,
#         models.JobAd.JobDescription == ad.JobDescription,
#         models.JobAd.Location == ad.Location
#     ).first()

#     if existing_ad:
#         # If an identical job ad already exists, return the existing one
#         return JobAdResponse(
#             BottomSalary=existing_ad.BottomSalary,
#             TopSalary=existing_ad.TopSalary,
#             JobDescription=existing_ad.JobDescription,
#             Location=existing_ad.Location,
#             Status=existing_ad.Status,
#             Skills=skills,
#             CreatedAt=existing_ad.CreatedAt,
#             UpdatedAt=existing_ad.UpdatedAt
#         )

#     # If no identical job ad exists, proceed with creating a new one
#     new_ad = models.JobAd(
#         CompanyID=id,
#         BottomSalary=ad.BottomSalary,
#         TopSalary=ad.TopSalary,
#         JobDescription=ad.JobDescription,
#         Location=ad.Location
#     )

#     db.add(new_ad)
#     db.flush()
#     db.commit()
#     db.refresh(new_ad)
#     add_skills_to_ad(new_ad.JobAdID, skills, db)
#     ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == new_ad.JobAdID).first()
#     names = get_names(id, db) # Useless :)))
#     return JobAdResponse(
#         BottomSalary=ad.BottomSalary,
#         TopSalary=ad.TopSalary,
#         JobDescription=ad.JobDescription,
#         Location=ad.Location,
#         Status=ad.Status,
#         Skills=skills,
#         CreatedAt=ad.CreatedAt,
#         UpdatedAt=ad.UpdatedAt
#     )
# ^^^^^^^ Тоя код не позволява да има абсолютно едни и същи job ad-ове 
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
    add_skills_to_ad(new_ad.JobAdID, skills, db)
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
    ad = db.query(models.JobAd.JobAdID).filter(models.JobAd.JobAdID == ad_id)
    for skill in skills:
        skill_id = db.query(models.Skill.SkillID).filter(models.Skill.Description == f"{skill}")
        db.add(models.JobAdSkill(JobAdID=ad, SkillID=skill_id))
        db.commit()


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
        res.append(schemas.JobAdResponse(
            BottomSalary=ad.BottomSalary,
            TopSalary=ad.TopSalary,
            JobDescription=ad.JobDescription,
            Location=ad.Location,
            Status=ad.Status,
            Skills=[' - '.join(skill) for skill in skills],
            CreatedAt=ad.CreatedAt,
            UpdatedAt=ad.UpdatedAt
        ))
    return res

def edit_job_ad(job_ad_id: int, new_ad: schemas.JobAdUpdate, db: Session):
    # Fetch the job ad
    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == job_ad_id).first()

    if not job_ad:
        return None  # Job ad not found

    if new_ad.Status and new_ad.Status not in ["Active", "Archived"]:
        # Raise an exception or return an error indicating invalid status.
        raise ValueError("Invalid status value")

    # Update the job ad fields as per the new_ad data
    job_ad.BottomSalary = new_ad.BottomSalary if new_ad.BottomSalary is not None else job_ad.BottomSalary
    job_ad.TopSalary = new_ad.TopSalary if new_ad.TopSalary is not None else job_ad.TopSalary
    job_ad.JobDescription = new_ad.JobDescription if new_ad.JobDescription is not None else job_ad.JobDescription
    job_ad.Location = new_ad.Location if new_ad.Location is not None else job_ad.Location
    job_ad.Status = new_ad.Status if new_ad.Status is not None else job_ad.Status

    # Update skills
    if new_ad.Skills is not None:
        # Clear existing skills
        db.query(models.JobAdSkill).filter(models.JobAdSkill.JobAdID == job_ad_id).delete()
        # Add new skills
        for skill in new_ad.Skills:
            skill_entry = db.query(models.Skill).filter(models.Skill.Description == skill).first()
            if not skill_entry:
                # If skill does not exist, add it to the database
                new_skill = models.Skill(Description=skill)
                db.add(new_skill)
                try:
                    db.commit()
                except IntegrityError:
                    db.rollback()  # Rollback in case the skill is already added concurrently
                    skill_entry = db.query(models.Skill).filter(models.Skill.Description == skill).first()
                else:
                    skill_entry = new_skill
            db.add(models.JobAdSkill(JobAdID=job_ad_id, SkillID=skill_entry.SkillID))

    # Commit changes to the database
    db.commit()
    return job_ad


def get_job_ad(job_ad_id: int, db: Session):
    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == job_ad_id).first()
    return job_ad


def get_skills_for_job_ad(db, ad):
    return db.query(models.Skill.Description, models.JobAdSkill.Level).join(
        models.JobAdSkill, models.JobAdSkill.SkillID == models.Skill.SkillID).join(
        models.JobAd, models.JobAd.JobAdID == models.JobAdSkill.JobAdID).filter(
        models.JobAd.JobAdID == ad.JobAdID).all()

