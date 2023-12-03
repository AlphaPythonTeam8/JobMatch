from typing import Optional
from fastapi_pagination import LimitOffsetPage, paginate
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from common import oauth2
from common.oauth2 import get_current_company
from data import models
from data.database import get_db
from data.schemas import JobAdResponse, JobAd
from data import schemas
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
# @job_ad_router.post('/create-job_ad', response_model=JobAdResponse)
# def create_ad(ad: JobAd, company_id=Depends(get_current_company), db: Session = Depends(get_db)):
#     skills = ad.Skills.split(', ')
#     professional_services.add_skills_to_db(skills, db)
#     return create_job_ad(company_id, skills, ad, db)
@job_ad_router.post('/create-job_ad', response_model=JobAdResponse)
def create_ad(
    user_id=Depends(get_current_company),
    bottom_salary: float = Form(...),
    top_salary: float = Form(...),
    job_description: str = Form(...),
    location: str = Form(...),
    status: str = Form(...),
    skills: str = Form(...),
    db: Session = Depends(get_db)
):
    ad = JobAd(
        BottomSalary=bottom_salary,
        TopSalary=top_salary,
        JobDescription=job_description,
        Location=location,
        Status=status,
        Skills=skills
    )

    skills_list = skills.split(', ')
    
    professional_services.add_skills_to_db(skills_list, db)
    
    return create_job_ad(user_id.CompanyID, skills_list, ad, db)




@job_ad_router.delete('/delete_job_ad/{job_ad_id}')
def delete_ad(job_ad_id: int, db: Session = Depends(get_db), company_id=Depends(get_current_company)):
    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == job_ad_id).first()

    if not job_ad:
        raise HTTPException(status_code=404, detail=f"Job ad such id does not exist")

    if job_ad.CompanyID != company_id.CompanyID:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job ad")

    db.delete(job_ad)
    db.commit()

    return JSONResponse(content={"message": f"JobAd with ID {job_ad_id} was successfully deleted"}, status_code=200)


@job_ad_router.put('/update_job_ad/{job_ad_id}')
def update_job_ad(job_ad_id: int, new_ad: schemas.JobAdUpdate, db: Session = Depends(get_db), company_id=Depends(oauth2.get_current_company)):
    # Check if the user is authorized to edit the job ad
    job_ad = jobad_services.get_job_ad(job_ad_id, db)
    if not job_ad:
        raise HTTPException(status_code=404, detail=f'Job ad with id {job_ad_id} does not exist')
    if job_ad.CompanyID != company_id.CompanyID:
        raise HTTPException(status_code=403, detail="Not authorized to edit this job ad")

    updated_ad = jobad_services.edit_job_ad(job_ad_id, new_ad, db)
    if not updated_ad:
        raise HTTPException(status_code=404, detail="Job ad not found")

    return updated_ad

@job_ad_router.get('/ads', response_model=LimitOffsetPage[JobAdResponse])
def get_all_ads(sort: str = 'asc', company_id=Depends(oauth2.get_current_company),
                db: Session = Depends(get_db)):
    ads = jobad_services.get_all_job_ads(company_id.CompanyID, sort, db)
    return paginate(ads)