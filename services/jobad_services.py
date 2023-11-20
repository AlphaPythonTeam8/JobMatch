from sqlalchemy.orm import Session
from data import schemas, models


def create_job_ad(company_id: int, skills, ad: schemas.JobAd, db: Session):
    new_job_ad = models.JobAd(CompanyID=company_id, SalaryRange=ad.SalaryRange,
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
