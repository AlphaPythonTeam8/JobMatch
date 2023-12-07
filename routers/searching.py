from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from services.searching_services import get_company_ads, read_companyads, get_job_ads, read_jobads, get_company_ads_in_salary_range
from services.searching_services import *
from data.database import get_db
from data.models import CompanyAd, JobAd
from common.oauth2 import get_current_company, get_current_professional

searching_router = APIRouter(tags=["Searching"])

@searching_router.get('/company_ads', description="Search By Location!")
def companies_search_for_company_ads(
    current_user: int = Depends(get_current_company),
    location: str | None = None,
    db: Session = Depends(get_db)
):
    if location:
        ads = get_company_ads(db, location)
    else:
        ads = read_companyads(db)

    result = []
    for CompanyAd in ads:
        ad_dict = {
            "bottom_sal": CompanyAd.BottomSalary,
            "top_sal": CompanyAd.TopSalary,
            "motivation": CompanyAd.MotivationDescription,
            "location": CompanyAd.Location,
            "status": CompanyAd.Status,
            "adrequirement": CompanyAd.CompanyAdRequirement
        }
        result.append(ad_dict)

    return result

@searching_router.get('/professionals', description="Company Searches Professional By Username!")
def companies_search_for_professionals(
    current_user: int = Depends(get_current_company),
    username: str | None = None,
    db: Session = Depends(get_db)
):
    if username:
        professionals = get_professional(db, username)
    else:
        professionals = read_professional(db)

    result = []
    for Professional in professionals:
        ad_dict = {
            "username": Professional.Username,
            "firstname": Professional.FirstName,
            "lastname": Professional.LastName,
            "email": Professional.ProfessionalEmail,
            "briefsummary": Professional.BriefSummary,
            "location": Professional.Location,
            "status": Professional.Status
        }
        result.append(ad_dict)

    return result

@searching_router.get('/companies', description="Company Searches Company By Company Name!")
def companies_search_for_other_companies(
    current_user: int = Depends(get_current_company),
    company_name: str | None = None,
    db: Session = Depends(get_db)
):
    if company_name:
        companies = get_company(db, company_name)
    else:
        companies = read_company(db)

    result = []
    for Company in companies:
        ad_dict = {
            "username": Company.Username,
            "company_name": Company.CompanyName,
            "description": Company.Description,
            "location": Company.Location,
            "email": Company.Email
        }
        result.append(ad_dict)

    return result

@searching_router.get('/job_ads', description="Professionals Search For Job Ads By Location")
def professionals_search_for_job_ads(
    current_user: int = Depends(get_current_professional),
    location: str | None = None,
    db: Session = Depends(get_db)
):
    if location:
        ads = get_job_ads(db, location)
    else:
        ads = read_jobads(db)

    result = []
    for JobAd in ads:
        ad_dict = {
            "company_id": JobAd.CompanyID,
            "bottom_sal": JobAd.BottomSalary,
            "top_sal": JobAd.TopSalary,
            "job_description": JobAd.JobDescription,
            "location": JobAd.Location,
            "status": JobAd.Status,
            "created_at": JobAd.CreatedAt,
            "updated_at": JobAd.UpdatedAt
        }
        result.append(ad_dict)

    return result

@searching_router.get('/company', description="Professional Searches Company By Company Name!")
def professionals_search_for_companies(
    current_user: int = Depends(get_current_professional),
    company_name: str | None = None,
    db: Session = Depends(get_db)
):
    if company_name:
        companies = get_company(db, company_name)
    else:
        companies = read_company(db)

    result = []
    for Company in companies:
        ad_dict = {
            "username": Company.Username,
            "company_name": Company.CompanyName,
            "description": Company.Description,
            "location": Company.Location,
            "email": Company.Email
        }
        result.append(ad_dict)

    return result

@searching_router.get('/professional', description="Professional Searches Professionals By Username!")
def professionals_search_for_professionals(
    current_user: int = Depends(get_current_professional),
    username: str | None = None,
    db: Session = Depends(get_db)
):
    if username:
        professionals = get_professional(db, username)
    else:
        professionals = read_professional(db)

    result = []
    for Professional in professionals:
        ad_dict = {
            "username": Professional.Username,
            "first_name": Professional.FirstName,
            "last_name": Professional.LastName,
            "status": Professional.Status,
            "email": Professional.ProfessionalEmail
        }
        result.append(ad_dict)

    return result

@searching_router.get('/job_ad', description="Salary Range Search For Job Ads")
def search_job_ads_by_salary_range(
    bottom_salary: float = None,
    top_salary: float = None,
    threshold: float = 0.0,
    db: Session = Depends(get_db)
):
    threshold /= 100

    if bottom_salary is not None:
        bottom_salary = bottom_salary - (bottom_salary * threshold)
    if top_salary is not None:
        top_salary = top_salary + (top_salary * threshold)

    job_ads = get_job_ads_in_salary_range(db, bottom_salary, top_salary)

    result = []
    for JobAd in job_ads:
        ad_dict = {
            "company_id": JobAd.CompanyID,
            "bottom_salary": JobAd.BottomSalary,
            "top_salary": JobAd.TopSalary,
            "job_description": JobAd.JobDescription,
            "location": JobAd.Location,
            "status": JobAd.Status,
            "created_at": JobAd.CreatedAt,
            "updated_at": JobAd.UpdatedAt,
        }
        result.append(ad_dict)

    return result

@searching_router.get('/company_ad', description="Salary Range Search For Company Ads")
def search_company_ads_by_salary_range(
    bottom_salary: float = None,
    top_salary: float = None,
    threshold: float = 0.0,
    db: Session = Depends(get_db)
):
    threshold /= 100

    if bottom_salary is not None:
        bottom_salary = bottom_salary - (bottom_salary * threshold)
    if top_salary is not None:
        top_salary = top_salary + (top_salary * threshold)

    company_ads = get_company_ads_in_salary_range(db, bottom_salary, top_salary)

    result = []
    for CompanyAd in company_ads:
        ad_dict = {
            "professional_id": CompanyAd.ProfessionalID,
            "bottom_salary": CompanyAd.BottomSalary,
            "top_salary": CompanyAd.TopSalary,
            "motivation_description": CompanyAd.MotivationDescription,
            "location": CompanyAd.Location,
            "status": CompanyAd.Status,
            "ad_requirement": CompanyAd.CompanyAdRequirement,
            "created_at": CompanyAd.CreatedAt,
            "updated_at": CompanyAd.UpdatedAt,
        }
        result.append(ad_dict)

    return result