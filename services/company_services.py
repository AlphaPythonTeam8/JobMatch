from common.hashing import hash_password
from common.oauth2 import generate_verification_token
from data import schemas, models
from sqlalchemy.orm import Session

from data.schemas import CompanyResponse, CompanyRegistration, CompanyUpdate
from services.email_services import send_verification_email


def register(user: schemas.CompanyRegistration, db: Session):
    """
    Register a new company account.

    Args:
        user (schemas.CompanyRegistration): The company registration information.
        db (Session): The database session.

    Returns:
        models.Company: The newly created company record.
    """

    # Hash the user's password
    hashed_password = hash_password(user.Password)
    user.Password = hashed_password

    # Generate a verification token
    verification_token = generate_verification_token()

    # Check if the email address is already in use
    existing_user = db.query(models.Company).filter(models.Company.Email == user.Email).first()
    if existing_user:
        return {"message": f"Email address {user.Email} is already in use."}

    # Create the company user
    company = models.Company(
        Username=user.Username,
        CompanyName=user.CompanyName,
        Email=user.Email,
        Password=user.Password,
        VerificationToken=verification_token,
        EmailVerified=False,
    )
    try:
        send_verification_email(company.Email, company.VerificationToken)
    except Exception as e:
        db.rollback()  # Undo the session changes because email sending failed
        raise HTTPException(status_code=500, detail=f"Failed to send verification email: {str(e)}")

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_company_by_username(db: Session, username: str):
    return db.query(models.Company).filter(models.Company.Username == username).first()


def get_company_by_id(db: Session, company_id: int):
    company_profile = db.query(models.Company).filter(models.Company.CompanyID == company_id).first()
    return company_profile


def get_company_name_by_id(db: Session, company_id: int):
    company_name = db.query(models.Company.CompanyName).filter(models.Company.CompanyID == company_id).first()
    return company_name[0] if company_name else None


def update_info(company_id: int, profile: schemas.CompanyUpdate, db: Session):
    update_data = profile.model_dump()

    # Perform the update operation
    profile_query = db.query(models.Company).filter(models.Company.CompanyID == company_id)
    profile_query.update(update_data, synchronize_session=False)
    db.commit()

    # Fetch the updated profile
    updated_profile = profile_query.first()

    if not updated_profile:
        return None

    # Calculate the count of active ads, similar to view_company_info
    count_ads = db.query(models.JobAd).filter(
        models.JobAd.CompanyID == company_id, models.JobAd.Status == "Active").count()

    # Return the CompanyResponse with fields matching those in view_company_info
    return CompanyResponse(
        Username=updated_profile.Username,
        CompanyName=updated_profile.CompanyName,
        Email=updated_profile.Email,
        Description=updated_profile.Description,
        Location=updated_profile.Location,
        PictureURL=updated_profile.PictureURL,
        Contact=updated_profile.Contact,
        ActiveAds=count_ads
    )


def view_company_info(company_id: int, db: Session):
    profile = db.query(models.Company).filter(models.Company.CompanyID == company_id).first()

    if not profile:
        return None

    count_ads = db.query(models.JobAd).filter(
        models.JobAd.CompanyID == company_id, models.JobAd.Status == "Active").count()

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


def get_match_requests_for_ad(company_id, db):
    return db.query(models.Match.MatchStatus, models.Match.SentAt, models.Professional.FirstName).join(
        models.Professional, models.Professional.ProfessionalID == models.Match.ProfessionalID).filter(
        models.Match.JobAdID == company_id).all()
