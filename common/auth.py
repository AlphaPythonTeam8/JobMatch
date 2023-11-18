from common import hashing
import oauth2
from data import database, schemas, models
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


auth_router = APIRouter(tags=['CompanyAuthentication'])


@auth_router.post('/login')
async def company_login(company_credentials: schemas.CompanyLogin, db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(models.Company.Username == company_credentials.username).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not hashing.verify(company_credentials.password, company.Password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    data = {"company_id": company.CompanyID}
    access_token = oauth2.create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}
