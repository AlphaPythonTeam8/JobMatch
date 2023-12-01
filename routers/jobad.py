from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from common import oauth2
from common.oauth2 import get_current_company
from data import models
from data.database import get_db
from data.schemas import JobAdResponse, JobAd
from services import company_services, jobad_services, professional_services
from services.jobad_services import create_job_ad
from services.professional_services import add_skills_to_ad

job_ad_router: APIRouter = APIRouter(
    prefix='/job_ad',
    tags=['JobAd']
)


# @job_ad_router.post('/create-job_ad', response_model=JobAdResponse)
# def create_ad(ad: JobAd, db: Session = Depends(get_db), company_id: int = Depends(get_current_company)):
#     # company_profile = company_services.get_company_by_id(db=db, company_id=company_id)
#     # if not company_profile:
#     #     raise HTTPException(status_code=404, detail=f'Company profile with id {company_id} does not exist.')
#     skills = ad.Skills.split(', ')
#     professional_services.add_skills_to_db(skills, db)
#     new_ad = jobad_services.create_job_ad(id, skills, ad, db)
#     return JobAdResponse(JobAdID=new_ad.JobAdID, CreatedAt=new_ad.CreatedAt)
@job_ad_router.post('/create-job_ad', response_model=JobAdResponse)
def create_ad(ad: JobAd, user_id=Depends(get_current_company), db: Session = Depends(get_db)):
    skills = ad.Skills.split(', ')
    professional_services.add_skills_to_db(skills, db)
    return create_job_ad(user_id.CompanyID, skills, ad, db)



@job_ad_router.delete('/delete_job_ad/{job_ad_id}')
def delete_ad(job_ad_id: int, db: Session = Depends(get_db), company=Depends(get_current_company)):

    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == job_ad_id).first()

    if not job_ad:
        raise HTTPException(status_code=404, detail=f"Job ad with id {job_ad_id} does not exist")

    if job_ad.CompanyID != company.CompanyID:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job ad")

    db.delete(job_ad)
    db.commit()

    return JSONResponse(content={"message": f"JobAd with ID {job_ad_id} was successfully deleted"}, status_code=200)

@job_ad_router.patch('/update_job_ad/{job_ad_id}')
def edit_job_ad(job_ad_id: int, bottom_salary: Optional[float] = None, top_salary: Optional[float] = None,
                job_description: Optional[str] = None, location: Optional[str] = None,
                status: Optional[str] = None, skills: Optional[str] = None,
                company_id=Depends(oauth2.get_current_company), db: Session = Depends(get_db)):

    # Get the job ad
    job_ad = jobad_services.get_job_ad(job_ad_id, db)
    if not job_ad:
        raise HTTPException(status_code=404, detail=f'Job ad with id {job_ad_id} does not exist')

    # Check if the user is authorized to edit the job ad
    if job_ad.CompanyID != company_id.CompanyID:
        raise HTTPException(status_code=403, detail="Not authorized to edit this job ad")

    # Update the JobAd object
    if bottom_salary is not None:
        job_ad.BottomSalary = bottom_salary
    if top_salary is not None:
        job_ad.TopSalary = top_salary
    if job_description is not None:
        job_ad.JobDescription = job_description
    if location is not None:
        job_ad.Location = location
    if status is not None:
        job_ad.Status = status

    # Update Skills
    if skills is not None:
        skill_list = skills.split(', ')
        professional_services.add_skills_to_db(skill_list, db)
        add_skills_to_ad(job_ad_id, skill_list, db)


    # Save the changes to the database
    db.commit()

    return jobad_services.edit_job_ad(job_ad, job_ad_id, db)



@job_ad_router.get("/", response_model=JobAd)
def get_all_ads(company_id=Depends(oauth2.get_current_company), db: Session = Depends(get_db)):
    return jobad_services.get_all_job_ads(company_id=company_id.CompanyID, db=db)