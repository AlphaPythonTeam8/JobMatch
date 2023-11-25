from common.hashing import hash_password
from common.oauth2 import generate_verification_token
from data import schemas, models
from sqlalchemy.orm import Session

from data.schemas import CompanyResponse
from services.email_services import send_verification_email


def register(user: schemas.CompanyRegistration, db: Session):
    hashed_password = hash_password(user.Password)
    user.Password = hashed_password
    verification_token = generate_verification_token()

    # Create the company user with the unverified email
    db_user = models.Company(
        Username = user.Username,
        CompanyName = user.CompanyName,
        Email = user.Email,
        Password = user.Password,
        VerificationToken = verification_token,
        EmailVerified = False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Send verification email
    # send_verification_email(db_user.Email, verification_token)

    return db_user


def get_company_by_username(db: Session, username: str):
    return db.query(models.Company).filter(models.Company.Username == username).first()


def get_company_by_id(db: Session, company_id: int):
    company_profile = db.query(models.Company).filter(models.Company.CompanyID == company_id).first()
    return company_profile


def get_company_name_by_id(db: Session, company_id: int):
    company_name = db.query(models.Company.CompanyName).filter(models.Company.CompanyID == company_id).first()
    return company_name[0] if company_name else None


def update_info(id: int, profile: schemas.Company, db: Session):
    profile_query = db.query(models.Company).filter(models.Company.CompanyID == id)
    profile_query.update(profile.model_dump(), synchronize_session=False)
    db.commit()
    return profile_query.first()


def view_company_info(id: int, db: Session):
    profile = db.query(models.Company).filter(models.Company.CompanyID == id).first()

    if not profile:
        return None

    count_ads = db.query(models.JobAd).filter(
        models.JobAd.CompanyID == id, models.JobAd.Status == "Active").count()

    return CompanyResponse(
        Username=profile.Username,
        CompanyName=profile.CompanyName,
        Email=profile.Email,
        Description=profile.Description,
        Location=profile.Location,
        PictureURL=profile.PictureURL,
        Contact=profile.Contact,
        ActiveAds=count_ads
    )
