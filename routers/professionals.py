from fastapi import APIRouter, Depends, HTTPException

from common import oauth2
from common.hashing import hash_password
from data.schemas import ProfessionalRegistration, ProfessionalBase, Professional, CompanyAd, CompanyAdResponse
from services import professional_services
from data.database import get_db
from sqlalchemy.orm import Session

from services.professional_services import ad_exists

professionals_router = APIRouter(prefix='/professionals', tags=['Professionals'])


@professionals_router.post('/register', response_model=ProfessionalBase)
def register(user: ProfessionalRegistration, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.Password)
    user.Password = hashed_password
    db_user = professional_services.get_pro_by_username(db, username=user.Username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return professional_services.register(user=user, db=db)

@professionals_router.get('/profile', response_model=Professional)
def get_personal_info(user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    profile = professional_services.get_pro_by_id(id=user_id.id, db=db)
    if not profile:
        raise HTTPException(status_code=404, detail=f'Professional profile with id {id} does not exist.')
    return profile


@professionals_router.put('/update-info', response_model=Professional)
def update_info(
        updated_profile: Professional,
        user_id=Depends(oauth2.get_current_professional),
        db: Session = Depends(get_db)):
    profile = professional_services.get_pro_by_id(id=user_id.id, db=db)
    if not profile:
        raise HTTPException(status_code=404, detail=f'Professional profile with id {id} does not exist.')
    return professional_services.update_info(user_id.id, updated_profile, db)


@professionals_router.post('/create-ad')
def create_ad(ad: CompanyAd, user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    profile = professional_services.get_pro_by_id(id=user_id.id, db=db)
    if not profile:
        raise HTTPException(status_code=404, detail=f'Professional profile with id {user_id.id} does not exist.')
    skills = ad.Skills.split(', ')
    professional_services.add_skills_to_db(skills, db)
    return professional_services.create_ad(user_id.id, skills, ad, db)


@professionals_router.get('/ads')
def get_all_ads(user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    return professional_services.get_all_ads(user_id.id, db)


@professionals_router.get('/{ad_id}')
def get_ad(ad_id: int, user_id=Depends(oauth2.get_current_professional), db: Session = Depends(get_db)):
    if not ad_exists(ad_id, db):
        raise HTTPException(status_code=404, detail=f'Company ad with id {ad_id} does not exist')



@professionals_router.put('/{id}/{ad_id}')
def edit_ad(id: int, ad_id: int):
    # Check if the ad exists first
    pass


@professionals_router.patch('/{id}/{ad_id}')
def set_main_ad(id: int, ad_id: int):
    # Maybe first check if there is not already set main ad
    pass












