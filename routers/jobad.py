from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from common import oauth2
from common.oauth2 import get_current_company
from data import models, schemas
from data.database import get_db
from data.schemas import JobAdResponse, JobAd, JobAdResponse2
from services import company_services, jobad_services, professional_services
from services.jobad_services import create_job_ad
from services.professional_services import add_skills_to_ad

job_ad_router: APIRouter = APIRouter(
    prefix='/job_ad',
    tags=['JobAd']
)


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
    """
    This function creates a new job ad.

    Args:
        user_id (Depends(get_current_company)): The user ID of the currently authenticated company.
        bottom_salary (float): The minimum salary for the job ad.
        top_salary (float): The maximum salary for the job ad.
        job_description (str): The description of the job.
        location (str): The location of the job.
        status (str): The status of the job ad (e.g. open, filled).
        skills (str): The skills required for the job, separated by commas.
        db (Session): The database session object.

    Returns:
        JobAdResponse: The newly created job ad.
    """
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
    """
    This function deletes a job ad.

    Args:
        job_ad_id (int): The ID of the job ad to be deleted.
        db (Session): The database session object.
        company_id (Depends(oauth2.get_current_company)): The company ID of the currently authenticated company.

    Returns:
        JSONResponse: A JSON response with a message indicating that the job ad was successfully deleted.
    """

    job_ad = db.query(models.JobAd).filter(models.JobAd.JobAdID == job_ad_id).first()

    if not job_ad:
        raise HTTPException(status_code=404, detail=f"Job ad such id does not exist")

    if job_ad.CompanyID != company_id.CompanyID:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job ad")

    db.delete(job_ad)
    db.commit()

    return JSONResponse(content={"message": f"JobAd with ID {job_ad_id} was successfully deleted"}, status_code=200)


@job_ad_router.put('/update_job_ad/{ad_id}')
def update_job_ad(
        ad_id: int,
        bottom_salary: int = Form(...),
        top_salary: int = Form(...),
        job_description: str = Form(...),
        location: str = Form(...),
        status: str = Form(...),
        skills: str = Form(...),
        db: Session = Depends(get_db),
        company_id=Depends(oauth2.get_current_company)
):
    """
    This function updates an existing job ad.

    Args:
        ad_id (int): The ID of the job ad to be updated.
        bottom_salary (int): The minimum salary for the job ad.
        top_salary (int): The maximum salary for the job ad.
        job_description (str): The description of the job.
        location (str): The location of the job.
        status (str): The status of the job ad (e.g. open, filled).
        skills (str): The skills required for the job, separated by commas.
        db (Session): The database session object.
        company_id (Depends(oauth2.get_current_company)): The company ID of the currently authenticated company.

    Returns:
        JobAdResponse: The updated job ad.
    """
    job_ad = jobad_services.get_job_ad(ad_id, db)
    if not job_ad:
        raise HTTPException(status_code=404, detail=f'Job ad with id {ad_id} does not exist')
    if job_ad.CompanyID != company_id.CompanyID:
        raise HTTPException(status_code=403, detail="Not authorized to edit this job ad")

    new_ad = schemas.JobAdUpdate(
        BottomSalary=bottom_salary,
        TopSalary=top_salary,
        JobDescription=job_description,
        Location=location,
        Status=status,
        Skills=skills
    )

    updated_ad = jobad_services.edit_job_ad(new_ad, ad_id, db)
    if not updated_ad:
        raise HTTPException(status_code=404, detail="Job ad not found")
    return updated_ad


@job_ad_router.get('/ads', response_model=LimitOffsetPage[JobAdResponse2])
def get_all_ads(sort: str = 'asc', company_id=Depends(oauth2.get_current_company),
                db: Session = Depends(get_db)):
    """
    This function gets all job ads.

    Args:
        sort (str): The sort order (ascending or descending).
        company_id (Depends(oauth2.get_current_company)): The company ID of the currently authenticated company.
        db (Session): The database session object.

    Returns:
        LimitOffsetPage[JobAdResponse2]: A paginated list of job ads.
    """
    ads = jobad_services.get_all_job_ads(company_id.CompanyID, sort, db)
    return paginate(ads)


@job_ad_router.get('/{ad_id}', response_model=JobAdResponse2)
def get_job_ad(ad_id: int, user_id=Depends(oauth2.get_current_company), db: Session = Depends(get_db)):
    """
    This function retrieves a specific job ad.

    Args:
        ad_id (int): The ID of the job ad to be retrieved.
        user_id (Depends(oauth2.get_current_company)): The user ID of the currently authenticated company.
        db (Session): The database session object.

    Returns:
        JobAdResponse2: The requested job ad.

    Raises:
        HTTPException: A HTTP exception is raised if the job ad does not exist or if the user is not authorized to view it.
    """
    ad = jobad_services.get_job_ad(ad_id, db)
    if not ad.CompanyID == user_id.CompanyID:
        raise HTTPException(status_code=403)
    if not ad:
        raise HTTPException(status_code=404, detail=f'Job ad with id {ad_id} does not exist')
    return jobad_services.return_job_ad(ad, db)
