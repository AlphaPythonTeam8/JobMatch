from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
import common.oauth2
from data.database import get_db
from data.schemas import CompanyBase, CompanyRegistration
from services import company_services

companies_router = APIRouter(prefix='/companies', tags=['Companies'])


@companies_router.post('/register', response_model=CompanyBase)
def register(company: CompanyRegistration, db: Session = Depends(get_db)):
    db_user = company_services.get_company_by_username(db, username=company.Username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return company_services.register(user=company, db=db)


@companies_router.get('/{id}')
def get_info(id: int):
    pass


@companies_router.put('/{id}')
def edit_info(id: int):
    pass




@companies_router.get('/{id}/{ad_id}')
def get_ad(id: int, ad_id: int):
    pass


@companies_router.put('/{id}/{ad_id}')
def edit_add(id: int, ad_id: int):
    pass


