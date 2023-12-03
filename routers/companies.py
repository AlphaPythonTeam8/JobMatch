from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from common import oauth2
from data.database import get_db
from data.schemas import CompanyBase, CompanyRegistration, CompanyResponse, CompanyUpdate
from services import company_services

companies_router = APIRouter(prefix='/companies', tags=['Companies'])


@companies_router.post('/register', response_model=CompanyBase)
def register(company: CompanyRegistration, db: Session = Depends(get_db)):
    db_user = company_services.get_company_by_username(db, username=company.Username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return company_services.register(user=company, db=db)


@companies_router.patch('/update-info', response_model=CompanyResponse)
def update_info(
        updated_profile: CompanyUpdate,
        company_id=Depends(oauth2.get_current_company),
        db: Session = Depends(get_db)):
    return company_services.update_info(company_id.CompanyID, updated_profile, db)

@companies_router.get('/profile', response_model=CompanyResponse)
def get_company_info(company_id=Depends(oauth2.get_current_company), db: Session = Depends(get_db)):
    company = company_services.view_company_info(company_id=company_id.CompanyID, db=db)
    return company