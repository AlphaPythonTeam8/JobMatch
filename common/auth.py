from common import hashing
from data.database import get_db
from data.models import Company, Professional
from . import oauth2
from data import database, schemas, models
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Query

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


professional_auth_router = APIRouter(prefix='/professional-login', tags=['ProfessionalAuthentication'])


@professional_auth_router.post('/')
async def professional_login(professional_credentials: OAuth2PasswordRequestForm = Depends(),
                             db: Session = Depends(database.get_db)):
    professional = db.query(models.Professional).filter(
        models.Professional.Username == professional_credentials.username).first()

    if not professional:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not hashing.verify(professional_credentials.password, professional.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    data = {"professional_id": professional.ProfessionalID}
    access_token = oauth2.create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}



@auth_router.get("/verify_email")
def verify_email(token: str, account_type: str = Query(default="company"), db: Session = Depends(get_db)):
    if account_type == "company":
        company = db.query(Company).filter(Company.VerificationToken == token).first()
        if company:
            company.EmailVerified = True
            db.commit()
            return {"message": "Email verified successfully"}
        elif company and company.EmailVerified:
            return {"message": "Email is already verified"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email token not found")
    elif account_type == "professional":
        professional = db.query(Professional).filter(Professional.VerificationToken == token).first()
        if professional:
            professional.EmailVerified = True
            db.commit()
            return {"message": "Email verified successfully"}
        elif professional and professional.EmailVerified:
            return {"message": "Email is already verified"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email token not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account type or token")

