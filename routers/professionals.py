from fastapi import APIRouter, Depends, HTTPException, Response, Form
from fastapi_pagination import LimitOffsetPage, paginate
from common import oauth2
from common.hashing import hash_password
from data.schemas import ProfessionalRegistration, ProfessionalBase, CompanyAd, CompanyAdResponse, \
    ProfessionalResponse, ProfessionalUpdate, CompanyAdResponseMatch
from services import professional_services
from data.database import get_db
from sqlalchemy.orm import Session


professionals_router = APIRouter(prefix='/professionals', tags=['Professionals'])


@professionals_router.post('/register', response_model=ProfessionalBase)
def register(user: ProfessionalRegistration, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.Password)
    user.Password = hashed_password
    db_user = professional_services.get_pro_by_username(db, username=user.Username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if professional_services.email_exists(db, user.ProfessionalEmail):
        raise HTTPException(status_code=400, detail='Email already registered.')
    return professional_services.register(user=user, db=db)


@professionals_router.get('/profile', response_model=ProfessionalResponse)
def get_personal_info(user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    profile = professional_services.get_pro(id=user_id.id, db=db)
    return profile


@professionals_router.patch('/update-info', response_model=ProfessionalResponse)
def update_info(
        updated_profile: ProfessionalUpdate,
        user_id=Depends(oauth2.get_current_professional),
        db: Session = Depends(get_db)):
    return professional_services.update_info(user_id.id, updated_profile, db)


# @professionals_router.post('/create-ad')
# def create_ad(ad: CompanyAd, user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
#     skills = ad.Skills.split(', ')
#     professional_services.add_skills_to_db(skills, db)
#     return professional_services.create_ad(user_id.id, skills, ad, db)
@professionals_router.post('/create-ad')
def create_ad(
    bottom_salary: int = Form(...),
    top_salary: int = Form(...),
    motivation_description: str = Form(...),
    location: str = Form(...),
    status: str = Form(...),
    skills: str = Form(...),
    company_ad_requirement: str = Form(...),
    user_id=Depends(oauth2.get_current_professional),
    db: Session = Depends(get_db)
):
    ad = CompanyAd(
        BottomSalary=bottom_salary,
        TopSalary=top_salary,
        MotivationDescription=motivation_description,
        Location=location,
        Status=status,
        Skills=skills,
        CompanyAdRequirement=company_ad_requirement
    )

    skills_list = skills.split(', ')
    professional_services.add_skills_to_db(skills_list, db)

    return professional_services.create_ad(user_id.id, skills_list, ad, db)


@professionals_router.get('/ads')
def get_all_ads(sort: str | None = None, user_id=Depends(oauth2.get_current_professional),
                db: Session = Depends(get_db)) -> LimitOffsetPage:
    return paginate(professional_services.get_all_ads(user_id.id, sort, db),)


@professionals_router.get('/{ad_id}', response_model=CompanyAdResponseMatch)
def get_ad(ad_id: int, user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    ad = professional_services.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail=f'Company ad with id {ad_id} does not exist')
    if not ad.ProfessionalID == user_id.id:
        raise HTTPException(status_code=403)
    return professional_services.return_ad(ad, db)


@professionals_router.put('/update_ad/{ad_id}')
def edit_ad(new_ad: CompanyAd, ad_id: int, user_id=Depends(oauth2.get_current_professional),
            db: Session = Depends(get_db)):
    ad = professional_services.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail=f'Company ad with id {ad_id} does not exist')
    if not ad.ProfessionalID == user_id.id:
        raise HTTPException(status_code=403)
    return professional_services.edit_ad(new_ad, ad_id, db)


@professionals_router.patch('/main-ad/{ad_id}')
def set_main_ad(ad_id: int, user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    ad = professional_services.get_ad(ad_id, db)
    if not ad or not ad.ProfessionalID == user_id.id:
        raise HTTPException(status_code=404)
    professional_services.set_main_ad(ad_id, user_id.id, db)
    return Response(status_code=200, content='Main company ad was set.')












