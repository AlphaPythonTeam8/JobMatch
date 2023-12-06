from data import schemas, models
from sqlalchemy.orm import Session
import sqlalchemy.exc
from data.schemas import CompanyAdResponse, CompanyAdsResponse, CompanyAdsResponse2, ProfessionalResponse, CompanyAdMatchRequest, \
    CompanyAdResponseMatch
from sqlalchemy import or_


def register(user: schemas.ProfessionalRegistration, db: Session):
    db_user = models.Professional(
        Username=user.Username,
        FirstName=user.FirstName,
        LastName=user.LastName,
        Password=user.Password,
        ProfessionalEmail=user.ProfessionalEmail
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_ads(id: int, sort, db: Session):
    res = []
    if sort == 'asc':
        order_query = models.CompanyAd.UpdatedAt.asc()
    else:
        order_query = models.CompanyAd.UpdatedAt.desc()
    ads = db.query(models.CompanyAd).join(
        models.CompanyAdSkill, models.CompanyAd.CompanyAdID == models.CompanyAdSkill.CompanyAdID).join(
        models.Skill, models.CompanyAdSkill.SkillID == models.Skill.SkillID
    ).filter(models.CompanyAd.ProfessionalID == id).order_by(order_query)
    for ad in ads:
        skills = get_skills(db, ad)
        res.append(CompanyAdsResponse2(
            CompanyAdID=ad.CompanyAdID,
            BottomSalary=ad.BottomSalary,
            TopSalary=ad.TopSalary,
            MotivationDescription=ad.MotivationDescription,
            Location=ad.Location,
            Skills=[' - '.join(skill) for skill in skills],
            Status=ad.Status,
            CompanyAdRequirement=ad.CompanyAdRequirement,
            CreatedAt=ad.CreatedAt,
            UpdatedAt=ad.UpdatedAt
        ))
    return res


def get_ad(id: int, db: Session):
    ad = db.query(models.CompanyAd).filter(models.CompanyAd.CompanyAdID == id).first()
    return ad


def return_ad(ad, db: Session):
    skills = get_skills(db, ad)
    names = get_names(ad.ProfessionalID, db)
    match_requests = get_match_requests_for_ad(ad.CompanyAdID, db)
    return CompanyAdResponseMatch(
        FirstName=names.FirstName,
        LastName=names.LastName,
        BottomSalary=ad.BottomSalary,
        TopSalary=ad.TopSalary,
        MotivationDescription=ad.MotivationDescription,
        Location=ad.Location,
        Skills=[' - '.join(skill) for skill in skills],
        Status=ad.Status,
        CreatedAt=ad.CreatedAt,
        UpdatedAt=ad.UpdatedAt,
        CompanyAdRequirement=ad.CompanyAdRequirement,
        MatchRequests=[CompanyAdMatchRequest(
            CompanyName=match_request.CompanyName,
            MatchStatus=match_request.MatchStatus,
            SentAt=match_request.SentAt
        ) for match_request in match_requests]

    )


def edit_ad(new_ad, id: int, db: Session):
    skills = new_ad.Skills.split(', ')
    add_skills_to_db(skills, db)
    add_skills_to_ad(id, skills, db)
    ad_query = db.query(models.CompanyAd).filter(models.CompanyAd.CompanyAdID == id)
    ad_query.update(dict(BottomSalary=new_ad.BottomSalary,
                         TopSalary=new_ad.TopSalary,
                         MotivationDescription=new_ad.MotivationDescription,
                         Location=new_ad.Location,
                         Status=new_ad.Status,
                         CompanyAdRequirement=new_ad.CompanyAdRequirement), synchronize_session=False)
    db.commit()
    new_ad = ad_query.first()
    names = get_names(new_ad.ProfessionalID, db)
    return CompanyAdResponse(
        FirstName=names.FirstName,
        LastName=names.LastName,
        BottomSalary=new_ad.BottomSalary,
        TopSalary=new_ad.TopSalary,
        MotivationDescription=new_ad.MotivationDescription,
        Location=new_ad.Location,
        Status=new_ad.Status,
        Skills=list(skills),
        CompanyAdRequirement=new_ad.CompanyAdRequirement,
        CreatedAt=new_ad.CreatedAt,
        UpdatedAt=new_ad.UpdatedAt
    )


def set_main_ad(ad_id: int, user_id: int, db: Session):
    ad_query = db.query(models.Professional).filter(models.Professional.ProfessionalID == user_id)
    ad_query.update(dict(MainAd=ad_id), synchronize_session=False)
    db.commit()


def create_ad(id: int, skills, ad: schemas.CompanyAd, db: Session):
    new_ad = models.CompanyAd(ProfessionalID=id,
                              BottomSalary=ad.BottomSalary,
                              TopSalary=ad.TopSalary,
                              MotivationDescription=ad.MotivationDescription,
                              Location=ad.Location,
                              CompanyAdRequirement=ad.CompanyAdRequirement)
    db.add(new_ad)
    db.flush()
    db.commit()
    db.refresh(new_ad)
    add_skills_to_ad(new_ad.CompanyAdID, skills, db)
    ad = db.query(models.CompanyAd).filter(models.CompanyAd.CompanyAdID == new_ad.CompanyAdID).first()
    names = get_names(id, db)
    return CompanyAdResponse(
        FirstName=names.FirstName,
        LastName=names.LastName,
        BottomSalary=ad.BottomSalary,
        TopSalary=ad.TopSalary,
        MotivationDescription=ad.MotivationDescription,
        Location=ad.Location,
        Skills=skills,
        Status=ad.Status,
        CreatedAt=ad.CreatedAt,
        UpdatedAt=ad.UpdatedAt,
        CompanyAdRequirement=ad.CompanyAdRequirement
    )


def get_pro_by_username(db: Session, username: str):
    return db.query(models.Professional).filter(models.Professional.Username == username).first()


def email_exists(db: Session, email: str):
    return db.query(models.Professional).filter(models.Professional.ProfessionalEmail == email).first()


def get_pro(id: int, db: Session):
    profile = db.query(models.Professional).filter(models.Professional.ProfessionalID == id).first()
    count_ads = db.query(models.CompanyAd).filter(
        models.CompanyAd.ProfessionalID == id, models.CompanyAd.Status == "Active").count()
    return ProfessionalResponse(
        Username=profile.Username,
        FirstName=profile.FirstName,
        LastName=profile.LastName,
        ProfessionalEmail=profile.ProfessionalEmail,
        BriefSummary=profile.BriefSummary,
        Location=profile.Location,
        Status=profile.Status,
        PhotoURL=profile.PhotoURL,
        CVURL=profile.CVURL,
        Contact=profile.Contact,
        ActiveAds=count_ads
    )


def update_info(id: int, profile: schemas.ProfessionalUpdate, db: Session):
    profile_query = db.query(models.Professional).filter(models.Professional.ProfessionalID == id)
    profile_query.update(profile.model_dump(), synchronize_session=False)
    db.commit()
    profile = profile_query.first()
    count_ads = db.query(models.CompanyAd).filter(models.CompanyAd.ProfessionalID == id,
                                                  models.CompanyAd.Status == "Active").count()
    return ProfessionalResponse(
        Username=profile.Username,
        FirstName=profile.FirstName,
        LastName=profile.LastName,
        ProfessionalEmail=profile.ProfessionalEmail,
        BriefSummary=profile.BriefSummary,
        Location=profile.Location,
        Status=profile.Status,
        PhotoURL=profile.PhotoURL,
        CVURL=profile.CVURL,
        Contact=profile.Contact,
        ActiveAds=count_ads
    )


def add_skills_to_db(skills, db: Session):
    for data in skills:
        skill, level = data.split(' - ')
        try:
            db.add(models.Skill(Description=skill))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            continue


# def add_skills_to_ad(ad_id: int, skills, db: Session):
#     db.query(models.CompanyAdSkill).filter(models.CompanyAdSkill.CompanyAdID == ad_id).delete()
#     for data in skills:
#         skill, level = data.split(' - ')
#         skill_id = db.query(models.Skill.SkillID).filter(models.Skill.Description == f"{skill}")
#         db.add(models.CompanyAdSkill(CompanyAdID=ad_id, SkillID=skill_id, Level=level))
#         db.commit()
def add_skills_to_ad(ad_id: int, skills, db: Session):
    db.query(models.CompanyAdSkill).filter(models.CompanyAdSkill.CompanyAdID == ad_id).delete()
    for data in skills:
        try:
            skill, level = data.split(' - ')
            skill_id = db.query(models.Skill.SkillID).filter(models.Skill.Description == f"{skill}")
            db.add(models.CompanyAdSkill(CompanyAdID=ad_id, SkillID=skill_id, Level=level))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            continue


def get_names(id, db):
    return db.query(models.Professional.FirstName,
                    models.Professional.LastName).filter(models.Professional.ProfessionalID == id).first()


def get_skills(db, ad):
    return db.query(models.Skill.Description, models.CompanyAdSkill.Level).join(
        models.CompanyAdSkill, models.CompanyAdSkill.SkillID == models.Skill.SkillID).join(
        models.CompanyAd, models.CompanyAd.CompanyAdID == models.CompanyAdSkill.CompanyAdID).filter(
        models.CompanyAd.CompanyAdID == ad.CompanyAdID).all()


def get_match_requests_for_ad(id, db):
    return db.query(models.Match.MatchStatus, models.Match.SentAt, models.Company.CompanyName).join(
        models.Company, models.Company.CompanyID == models.Match.CompanyID).filter(
        models.Match.CompanyAdID == id).all()


def change_password(professional_id: int, new_password: str, db: Session):
    db.query(models.Professional).filter(models.Professional.ProfessionalID == professional_id).update(
        {models.Professional.Password: new_password})
    db.commit()


def get_sent_match_requests(user_id: int, db: Session):
    requests = db.query(models.Match, models.Company.CompanyName).join(
        models.Company, models.Company.CompanyID == models.Match.CompanyID, isouter=True).filter(
        models.Match.ProfessionalID == user_id).filter(models.Match.InitializedBy == 'Professional').order_by(
        models.Match.SentAt.desc())
    print(requests)
    result = []
    for match,company in requests:
        result.append({
            'Company': company,
            'JobAdID': match.JobAdID,
            'Status': match.MatchStatus,
            'Created': match.SentAt
        })
    return result


def get_received_match_requests(user_id: int, db: Session):
    requests = db.query(models.Match, models.Company.CompanyName).join(models.Company,
        models.Company.CompanyID == models.Match.CompanyID,isouter=True).join(
        models.CompanyAd, models.CompanyAd.CompanyAdID == models.Match.CompanyAdID, isouter=True).filter(
        or_(models.Match.ProfessionalID == user_id, models.CompanyAd.ProfessionalID == user_id)).filter(
        models.Match.InitializedBy == 'Company'
    ).order_by(models.Match.SentAt.desc())
    result = []
    for request,company in requests:
        result.append({
            'CompanyID': company,
            'CompanyAdID': request.CompanyAdID,
            'Status': request.MatchStatus,
            'Created': request.SentAt
        })
    return result
