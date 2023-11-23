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