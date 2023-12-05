from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from common.hashing import hash_password
from common.oauth2 import get_current_admin
from data.database import get_db
from data.models import Admin, Company, Professional, JobAd, CompanyAd
from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE")

admin_router: APIRouter = APIRouter(prefix='/admin', tags=['Admin'])


class AdminRegistrationRequest(BaseModel):
    username: str
    password: str
    registration_code: str  # ADMIN_REGISTRATION_CODE


class BlockRequest(BaseModel):
    is_blocked: bool


def verify_registration_code(registration_code: str):
    """
    Verifies that the provided registration code is valid.

    Args:
        registration_code (str): The registration code to be verified.

    Raises:
        HTTPException: If the provided registration code is invalid.

    """
    if registration_code != ADMIN_REGISTRATION_CODE:
        raise HTTPException(
            status_code=403,
            detail="Invalid registration code"
        )


@admin_router.post("/register")
def create_admin(
        admin_request: AdminRegistrationRequest = Body(..., embed=True),
        db: Session = Depends(get_db)  # The database session object
):
    """
    Creates a new admin user.

    Args:
        admin_request (AdminRegistrationRequest): The request body containing the admin's username, password, and registration code.
        db (Session): The database session object.

    Returns:
        JSON: A JSON object containing a message indicating that the admin was created successfully.

    Raises:
        HTTPException: If the provided registration code is invalid.
    """
    # Verify the provided registration code
    verify_registration_code(admin_request.registration_code)

    # Use common.hashing to hash the password
    hashed_password = hash_password(admin_request.password)
    new_admin = Admin(
        Username=admin_request.username,
        Password=hashed_password
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "Admin user created successfully"}


@admin_router.put("/block_company/{company_id}")
def block_company(
        company_id: int,  # The ID of the company user to be blocked
        block_request: BlockRequest,
        db: Session = Depends(get_db),
        _: Admin = Depends(get_current_admin)  # The current authenticated admin user
):
    """
    Blocks or unblocks a company user.

    Args:
        company_id (int): The ID of the company user to be blocked.
        block_request (BlockRequest): The request body containing the block status.
        db (Session): The database session object.
        _: The current authenticated admin user.

    Returns:
        JSON: A JSON object containing a message indicating that the company user's block status was updated successfully.

    Raises:
        HTTPException: If the company user with the specified ID cannot be found.
    """
    company_user = db.query(Company).filter(Company.CompanyID == company_id).first()
    if not company_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company user not found")

    company_user.is_blocked = block_request.is_blocked
    db.commit()
    db.refresh(company_user)
    return {"message": "Company user block status updated"}


@admin_router.put("/block_professional/{professional_id}")
def block_professional(
        professional_id: int,  # The ID of the professional user to be blocked
        block_request: BlockRequest,
        db: Session = Depends(get_db),
        _: Admin = Depends(get_current_admin)  # The current authenticated admin user
):
    """
    Blocks or unblocks a professional user.

    Args:
        professional_id (int): The ID of the professional user to be blocked.
        block_request (BlockRequest): The request body containing the block status.
        db (Session): The database session object.
        _: The current authenticated admin user.

    Returns:
        JSON: A JSON object containing a message indicating that the professional user's block status was updated successfully.

    Raises:
        HTTPException: If the professional user with the specified ID cannot be found.
    """

    professional_user = db.query(Professional).filter(Professional.ProfessionalID == professional_id).first()
    if not professional_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professional user user not found")

    professional_user.is_blocked = block_request.is_blocked
    db.commit()
    db.refresh(professional_user)
    return {"message": "Professional user block status updated"}


@admin_router.delete('/delete_job_ad/{job_ad_id}')
def delete_job_ad(
        job_ad_id: int,  # The ID of the job ad to be deleted
        db: Session = Depends(get_db),
        _: Admin = Depends(get_current_admin)  # The current authenticated admin user
):
    """
    Deletes a job ad.

    Args:
        job_ad_id (int): The ID of the job ad to be deleted.
        db (Session): The database session object.
        _: The current authenticated admin user.

    Returns:
        JSONResponse: A JSON response containing a message indicating that the job ad was deleted successfully.

    Raises:
        HTTPException: If the job ad with the specified ID cannot be found.
    """

    job_ad = db.query(JobAd).filter(JobAd.JobAdID == job_ad_id).first()

    if not job_ad:
        raise HTTPException(status_code=404, detail=f"Job ad such id does not exist")

    db.delete(job_ad)
    db.commit()

    return JSONResponse(content={"message": f"JobAd with ID {job_ad_id} was successfully deleted"}, status_code=200)


@admin_router.delete('/delete_company_ad/{company_ad_id}')
def delete_company_ad(
        company_ad_id: int,  # The ID of the company ad to be deleted
        db: Session = Depends(get_db),
        _: Admin = Depends(get_current_admin)  # The current authenticated admin user
):
    """
    Deletes a company ad.

    Args:
        company_ad_id (int): The ID of the company ad to be deleted.
        db (Session): The database session object.
        _: The current authenticated admin user.

    Returns:
        JSONResponse: A JSON response containing a message indicating that the company ad was deleted successfully.

    Raises:
        HTTPException: If the company ad with the specified ID cannot be found.
    """
    company_ad = db.query(CompanyAd).filter(CompanyAd.CompanyAdID == company_ad_id).first()

    if not company_ad:
        raise HTTPException(status_code=404, detail=f"Job ad such id does not exist")

    db.delete(company_ad)
    db.commit()

    return JSONResponse(content={"message": f"CompanyAd with ID {company_ad_id} was successfully deleted"},
                        status_code=200)
