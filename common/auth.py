from common import hashing
from config import JWT_SECRET_KEY

from data import database, schemas, models
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

router = APIRouter(tags=['CompanyAuthentication'])


@router.post('/login')
async def company_login(company_credentials: schemas.CompanyLogin, db: Session = Depends(database.get_db())):
    company = db.query(models.Company).filter(models.Company.username == company_credentials.username).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not hashing.verify(company_credentials.password, company.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    return {"token": "example_token"}
