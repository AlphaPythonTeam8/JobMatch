from http.client import HTTPException

from sqlalchemy.orm import Session
from data import schemas, models
from data.schemas import JobAdResponse
from services.company_services import get_company_name_by_id
from services.professional_services import add_skills_to_db, add_skills_to_ad


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


def get_all_job_ads(company_id: int, db: Session):
    res = []
    ads = db.query(models.JobAd).join(
        models.JobAdSkill, models.JobAd.JobAdID == models.JobAdSkill.JobAdID).join(
        models.Skill, models.JobAdSkill.SkillID == models.Skill.SkillID
    ).filter(models.JobAd.CompanyID == company_id).all()
    for ad in ads:
        skills = db.query(models.Skill.Description, models.CompanyAdSkill.Level).join(
            models.JobAdSkill, models.JobAdSkill.SkillID == models.Skill.SkillID).join(
            models.JobAd, models.JobAd.JobAdID == models.JobAdSkill.JobAdID).filter(
            models.JobAd.JobAdID == ad.JobAdID).all()
        # print([' - '.join(skill) for skill in skills])
        res.append(schemas.JobAd(
            SalaryRange=ad.SalaryRange,
            JobDescription='Test',
            MotivationDescription=ad.MotivationDescription,
            Location=ad.Location,
            JobRequirement='Test',
            Skills=[' - '.join(skill) for skill in skills],
            Status=ad.Status
        ))
    return res


def edit_job_ad(new_ad: schemas.JobAd, id: int, db: Session):
    # Fetch the existing job ad from the database
    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == id).first()

    # Check if job ad exists
    if not job_ad:
        raise HTTPException(status_code=404, detail=f"Job ad with id {id} does not exist")

    # Update the JobAd attributes
    job_ad.BottomSalary = new_ad.BottomSalary if new_ad.BottomSalary is not None else job_ad.BottomSalary
    job_ad.TopSalary = new_ad.TopSalary if new_ad.TopSalary is not None else job_ad.TopSalary
    job_ad.JobDescription = new_ad.JobDescription if new_ad.JobDescription is not None else job_ad.JobDescription
    job_ad.Location = new_ad.Location if new_ad.Location is not None else job_ad.Location
    job_ad.Status = new_ad.Status if new_ad.Status is not None else job_ad.Status

    # Update Skills separately if provided
    if new_ad.Skills is not None:
        skills = new_ad.Skills.split(', ')
        add_skills_to_db(skills, db)
        add_skills_to_job_ad(id, skills, db)

    # Commit changes to the database
    db.commit()

    # Refresh the job_ad object to get the updated data from the database
    db.refresh(job_ad)

    # Fetch company name for the response
    company_name = get_company_name_by_id(db, job_ad.CompanyID)

    # Construct and return the response
    return JobAdResponse(
        CompanyName=company_name,
        BottomSalary=job_ad.BottomSalary,
        TopSalary=job_ad.TopSalary,
        JobDescription=job_ad.JobDescription,
        Location=job_ad.Location,
        Status=job_ad.Status,
        Skills=skills if new_ad.Skills is not None else None,
        CreatedAt=job_ad.CreatedAt,
        UpdatedAt=job_ad.UpdatedAt
    )


def get_job_ad(id: int, db: Session):
    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == id).first()
    return job_ad
