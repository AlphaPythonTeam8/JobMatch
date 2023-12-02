from sqlalchemy.orm import Session
from fastapi import Response
import sqlalchemy.exc
from data import models
from services import jobad_services as ja, professional_services as p


def send_request_to_job_ad(ad_id: int, professional_id: int, db: Session):
    new_request = models.Match(ProfessionalID=professional_id, JobAdID=ad_id, InitializedBy='Professional')
    db.add(new_request)
    db.commit()
    return Response(status_code=200, content='Match request was sent successfully.')


def send_request_to_company_ad(ad_id: int, company_id: int, db: Session):
    new_request = models.Match(CompanyID=company_id, CompanyAdID=ad_id, InitializedBy='Company')
    db.add(new_request)
    db.commit()
    return Response(status_code=200, content='Match request was sent successfully.')


def company_professional_request(company_id: int, professional_id: int, db: Session, initialized_by: str):
    try:
        new_request = models.Match(ProfessionalID=professional_id, CompanyID=company_id, InitializedBy=initialized_by)
        db.add(new_request)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        return Response(status_code=404)
    return Response(status_code=200, content='Match request was sent successfully.')


def get_job_ad_request(professional_id, ad_id, db):
    return db.query(models.Match).filter(
        models.Match.ProfessionalID == professional_id, models.Match.JobAdID == ad_id).first()


def get_company_ad_request(company_id, ad_id, db):
    return db.query(models.Match).filter(
        models.Match.CompanyID == company_id, models.Match.CompanyAdID == ad_id).first()


def get_professional_company_request(professional_id, company_id, db, initialized_by: str):
    return db.query(models.Match).filter(models.Match.ProfessionalID == professional_id,
                                         models.Match.CompanyID == company_id,
                                         models.Match.InitializedBy == initialized_by).first()


def match_request_exists_by_id(id: int, db: Session):
    return db.query(models.Match).filter(models.Match.RequestID == id).first()


def reject_match_request(request_id, db: Session):
    db.query(models.Match).filter(models.Match.RequestID == request_id).update({models.Match.MatchStatus: 'Rejected'})
    db.commit()
    return Response(status_code=200, content='Match request was rejected.')


def professional_accept_request(professional_id: int, request_id: int, db: Session):
    match_request = match_request_exists_by_id(request_id, db)
    db.query(models.Match).filter(models.Match.RequestID == request_id).update({models.Match.MatchStatus: 'Accepted'})
    db.query(models.Professional).filter(models.Professional.ProfessionalID == professional_id).update(
        {models.Professional.Status: 'Busy'})
    if match_request.CompanyAdID:
        db.query(models.CompanyAd).filter(models.CompanyAd.CompanyAdID == match_request.CompanyAdID).update(
            {models.CompanyAd.Status: 'Archived'})
    db.commit()
    return Response(status_code=200, content='Match request was accepted.')


def company_accept_request(company_id: int, request_id: int, db: Session):
    match_request = match_request_exists_by_id(request_id, db)
    db.query(models.Match).filter(models.Match.RequestID == request_id).update({models.Match.MatchStatus: 'Accepted'})
    db.query(models.Professional).filter(models.Professional.ProfessionalID == match_request.ProfessionalID).update(
        {models.Professional.Status: 'Busy'})
    if match_request.JobAdID:
        db.query(models.JobAd).filter(models.JobAd.JobAdID == match_request.JobAdID).update(
            {models.JobAd.Status: 'Archived'})
    db.commit()
    return Response(status_code=200, content='Match request was accepted.')


def company_own_request(current_company: int, match_request, db: Session):
    if match_request.JobAdID:
        job_ad = ja.get_job_ad(match_request.JobAdID, db)
        if not job_ad.CompanyID == current_company:
            return False
    elif not match_request.CompanyID == current_company:
        return False
    return True


def professional_own_request(current_professional: int, match_request, db: Session):
    if match_request.CompanyAdID:
        company_ad = p.get_ad(match_request.CompanyAdID, db)
        if not company_ad.ProfessionalID == current_professional:
            return False
    elif not match_request.ProfessionalID == current_professional:
        return False
    return True
