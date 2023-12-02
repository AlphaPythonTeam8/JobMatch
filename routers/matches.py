from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from common import oauth2
from data.database import get_db
from services import match_services, professional_services

matches_router = APIRouter(prefix='/match_requests', tags=['Match Requests'])


@matches_router.post('/job-ad/{job_ad_id}')
def send_match_request_to_job_ad(job_ad_id: int, user=Depends(oauth2.get_current_professional),
                                 db: Session = Depends(get_db)):
    # if not professional_services.get_ad(id, db):
    #     raise HTTPException(status_code=404)
    if match_services.get_job_ad_request(user.id, job_ad_id, db):
        raise HTTPException(status_code=400, detail='Match request is already sent.')
    return match_services.send_request_to_job_ad(job_ad_id, user.id, db)


@matches_router.post('/company-ad/{company_ad_id}')
def send_match_request_to_company_ad(company_ad_id: int, company=Depends(oauth2.get_current_company),
                                     db: Session = Depends(get_db)):
    if not professional_services.get_ad(company_ad_id, db):
        raise HTTPException(status_code=404)
    if match_services.get_company_ad_request(company.CompanyID, company_ad_id, db):
        raise HTTPException(status_code=400, detail='Match request is already sent.')
    return match_services.send_request_to_company_ad(company_ad_id, company.CompanyID, db)


@matches_router.post('/company/{company_id}')
def send_match_request_to_company(company_id: int, professional=Depends(oauth2.get_current_professional),
                                  db: Session = Depends(get_db)):
    match_request = match_services.get_professional_company_request(professional.id, company_id, db, 'Professional')
    if match_request:
        raise HTTPException(status_code=400, detail='Match request already exists.')
    return match_services.company_professional_request(company_id, professional.id, db, 'Professional')


@matches_router.post('/professional/{professional_id}')
def send_match_request_to_professional(professional_id: int, company=Depends(oauth2.get_current_company),
                                       db: Session = Depends(get_db)):
    match_request = match_services.get_professional_company_request(professional_id, company.CompanyID, db, 'Company')
    if match_request:
        raise HTTPException(status_code=400, detail='Match request already exists.')
    return match_services.company_professional_request(company.CompanyID, professional_id, db, 'Company')


@matches_router.patch('/professional/{request_id}')
def professional_process_request(action: Annotated[str, Body(pattern='^accept$|^reject')], request_id: int,
                                 professional=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    match_request = match_services.match_request_exists_by_id(request_id, db)
    if not match_services.professional_own_request(professional.id, match_request, db):
        raise HTTPException(status_code=403)
    if not match_request or match_request.InitializedBy == 'Professional':
        raise HTTPException(status_code=404)
    if not match_request.MatchStatus == 'Pending':
        raise HTTPException(status_code=400, detail='The match request is already processed by you.')
    if action == 'accept':
        return match_services.professional_accept_request(professional.id, request_id, db)
    else:
        return match_services.reject_match_request(request_id, db)


@matches_router.patch('/company/{request_id}')
def company_process_request(action: Annotated[str, Body(pattern='^accept$|^reject')], request_id: int,
                            company=Depends(oauth2.get_current_company), db: Session = Depends(get_db)):
    match_request = match_services.match_request_exists_by_id(request_id, db)
    if not match_services.company_own_request(company.CompanyID, match_request, db):
        raise HTTPException(status_code=403)
    if not match_request or match_request.InitializedBy == 'Company':
        raise HTTPException(status_code=404)
    if not match_request.MatchStatus == 'Pending':
        raise HTTPException(status_code=400, detail='The match request is already processed by you.')
    if action == 'accept':
        return match_services.company_accept_request(company.CompanyID, request_id, db)
    else:
        return match_services.reject_match_request(request_id, db)
