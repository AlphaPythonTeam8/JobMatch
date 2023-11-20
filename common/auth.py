from common import hashing
from . import oauth2
from data import database, schemas, models
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

auth_router = APIRouter(tags=['CompanyAuthentication'])


@auth_router.post('/login', response_model=schemas.Token)
async def company_login(company_credentials: OAuth2PasswordRequestForm = Depends(),
                        db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(models.Company.Username == company_credentials.username).first()

    if not company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not hashing.verify(company_credentials.password, company.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    data = {"company_id": company.CompanyID}
    access_token = oauth2.create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}
