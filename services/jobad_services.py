from sqlalchemy.orm import Session
from data import schemas, models


def create_job_ad(id: int, skills, ad: schemas.JobAd, db: Session):
    new_job_ad = models.JobAd(CompanyID=id, SalaryRange=ad.SalaryRange,
                              JobDescription=ad.JobDescription, Location=ad.Location, JobRequirement=ad.JobRequirement)
    db.add(new_job_ad)
    db.commit()
    db.refresh(new_job_ad)

    add_skills_to_job_ad(new_job_ad.JobAdID, skills, db)
    return new_job_ad


def add_skills_to_job_ad(ad_id: int, skills, db: Session):
    ad = db.query(models.JobAd.JobAdID).filter(models.JobAd.JobAdID == ad_id)
    for skill in skills:
        skill_id = db.query(models.Skill.SkillID).filter(models.Skill.Description == f"{skill}")
        db.add(models.JobAdSkill(JobAdID=ad, SkillID=skill_id))
        db.commit()
