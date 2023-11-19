from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.oauth2 import get_current
from data.database import get_db
from data.models import CompanyAd
from data.schemas import JobAdResponse
from services import company_services, jobad_services, professional_services

router = APIRouter(
    prefix='/job_ad',
    tags=['JobAd']
)


@router.post('/create-job_ad', response_model=JobAdResponse)
def create_ad(ad: CompanyAd, db: Session = Depends(get_db), company_id: int = Depends(get_current)):
    company_profile = company_services.get_company_by_id(id=company_id, db=db)
    if not company_profile:
        raise HTTPException(status_code=404, detail=f'Company profile with id {id} does not exist.')
    skills = ad.Skills.split(', ')
    professional_services.add_skills_to_db(skills, db)
    new_ad = jobad_services.create_job_ad(id, ad, db)
    return JobAdResponse(JobAdID=new_ad.JobAdID, CreatedAt=new_ad.CreatedAt)
