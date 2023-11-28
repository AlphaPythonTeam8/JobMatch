from sqlalchemy.orm import Session
from data.models import CompanyAd, JobAd, Professional, Company  # Replace with your actual import path

def get_company_ads(db: Session, search: str):
    data = (
        db.query(CompanyAd)
        .filter(CompanyAd.Location.ilike(f"%{search}%"))
        .all()
    )

    return data

def get_job_ads(db: Session, search: str):
    data = (
        db.query(JobAd)
        .filter(JobAd.Location.ilike(f"%{search}%"))
        .all()
    )

    return data


def read_companyads(db: Session):
    ads = db.query(CompanyAd).all()
    return ads

def read_jobads(db: Session):
    ads = db.query(JobAd).all()
    return ads

def get_professional(db: Session, search: str):
    data = (
        db.query(Professional)
        .filter(Professional.Username.ilike(f"%{search}%"))
        .all()
    )
    return data

def read_professional(db: Session):
    ads = db.query(Professional).all()
    return ads

def get_company(db: Session, search: str):
    data = (
        db.query(Company)
        .filter(Company.CompanyName.ilike(f"%{search}%"))
        .all()
    )
    return data

def read_company(db: Session):
    ads = db.query(Company).all()
    return ads

def get_job_ads_in_salary_range(db: Session, bottom_salary: float, top_salary: float):
    query = db.query(JobAd)
    
    if bottom_salary is not None and top_salary is not None:
        return query.filter(JobAd.BottomSalary >= bottom_salary, JobAd.TopSalary <= top_salary).all()
    elif bottom_salary is not None:
        return query.filter(JobAd.BottomSalary >= bottom_salary).all()
    elif top_salary is not None:
        return query.filter(JobAd.TopSalary <= top_salary).all()
    else:
        return query.all()