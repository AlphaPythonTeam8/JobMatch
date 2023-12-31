from common import hashing
from common.hashing import hash_password
from data.database import get_db
from data.models import Company, Professional, Admin
from common import oauth2
from data import database, schemas, models
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Query
from data.schemas import ChangePassword
from services import professional_services
from services.company_services import change_password

auth_router = APIRouter(tags=['CompanyAuthentication'])
admin_auth_router = APIRouter(prefix='/admin-login', tags=['AdminAuthentication'])


@auth_router.post('/login', response_model=schemas.Token)
async def company_login(company_credentials: OAuth2PasswordRequestForm = Depends(),
                        db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(models.Company.Username == company_credentials.username).first()

    if not company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not hashing.verify(company_credentials.password, company.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if company.is_blocked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")

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

    if professional.is_blocked == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")

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


@auth_router.post('/change-password')
def change_company_password(
        password_change: ChangePassword,
        company=Depends(oauth2.get_current_company),
        db: Session = Depends(get_db)
):
    return change_password(company.CompanyID, password_change.new_password, password_change.confirm_new_password, db)


@professional_auth_router.post('/change-password')
def change_professional_password(password_change: ChangePassword,
                                 professional=Depends(oauth2.get_current_professional),
                                 db: Session = Depends(get_db)):
    hashed_password = hashing.hash_password(password_change.new_password)
    professional_services.change_password(professional.id, hashed_password, db)
    return Response(status_code=200, content='Password was successfully updated.')


@admin_auth_router.post('/')
async def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(),
                      db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(
        models.Admin.Username == admin_credentials.username).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not hashing.verify(admin_credentials.password, admin.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    data = {"admin_id": admin.AdminID}
    access_token = oauth2.create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}


@admin_auth_router.post('/change-password')
async def change_admin_password(
        password_change: ChangePassword,
        admin=Depends(oauth2.get_current_admin),
        db: Session = Depends(get_db)
):
    hashed_new_password = hashing.hash_password(password_change.new_password)
    if password_change.new_password != password_change.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match"
        )
    admin.Password = hashed_new_password
    db.commit()
    return Response(status_code=200, content='Password was successfully updated.')

