from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.oauth2 import get_current_company
from data.database import get_db
from data.schemas import JobAdResponse, JobAd
from services import company_services, jobad_services, professional_services
from services.jobad_services import create_job_ad

job_ad_router = APIRouter(
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



@job_ad_router.delete('/delete_job_ad', response_model=JobAdResponse)
def delete_ad(ad: JobAd, db: Session = Depends(get_db), company: int = Depends(get_current_company)):

    pass


@job_ad_router.patch('/update_job_ad', response_model=JobAdResponse)
def update_ad(ad: JobAd, db: Session = Depends(get_db), company: int = Depends(get_current_company)):

    pass

@job_ad_router.get("/", response_model=JobAd)
def get_all_ads(db: Session = Depends(get_db), company: int = Depends(get_current_company)):
    return jobad_services.get_all_job_ads(company, db)

