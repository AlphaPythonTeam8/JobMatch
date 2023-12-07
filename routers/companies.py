from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common import oauth2
from data.database import get_db
from data.schemas import CompanyBase, CompanyRegistration, CompanyResponse, CompanyUpdate
from services import company_services
from data.models import Company

# Define the companies router
companies_router = APIRouter(prefix='/companies', tags=['Companies'])


# Define the register endpoint
@companies_router.post('/register', response_model=CompanyBase)
def register(company: CompanyRegistration, db: Session = Depends(get_db)):
    """
    Register a new company.

    Args:
        company (CompanyRegistration): The company details to register.
        db (Session): The database session.

    Returns:
        CompanyBase: The registered company details.

    Raises:
        HTTPException: If the username is already registered.
    """
    # Check if the username is already registered
    db_user = company_services.get_company_by_username(db, username=company.Username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return company_services.register(user=company, db=db)


# Define the update_info endpoint
@companies_router.patch('/update-info', response_model=CompanyResponse)
def update_info(
        updated_profile: CompanyUpdate,
        company_id=Depends(oauth2.get_current_company),
        db: Session = Depends(get_db)):
    """
    Update the company information.

    Args:
        updated_profile (CompanyUpdate): The updated company information.
        company_id (int): The company ID.
        db (Session): The database session.

    Returns:
        CompanyResponse: The updated company details.
    """
    # Update the company information
    return company_services.update_info(company_id.CompanyID, updated_profile, db)


# Define the get_company_info endpoint
@companies_router.get('/profile', response_model=CompanyResponse)
def get_company_info(company_id=Depends(oauth2.get_current_company), db: Session = Depends(get_db)):
    """
    Get the company information.

    Args:
        company_id (int): The company ID.
        db (Session): The database session.

    Returns:
        CompanyResponse: The company details.
    """
    # Get the company information
    company = company_services.view_company_info(company_id=company_id.CompanyID, db=db)
    return company


# Define the delete_profile endpoint
@companies_router.delete('/delete')
def delete_profile(company: Company = Depends(oauth2.get_current_company), db: Session = Depends(get_db)):
    """
    Delete the company profile.

    Args:
        company (Company): The company details.
        db (Session): The database session.

    Returns:
        dict: A message indicating that the profile was deleted successfully.
    """
    # Delete the company profile
    db.delete(company)
    db.commit()
    return {"message": "Profile deleted successfully"}
