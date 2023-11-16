from fastapi import APIRouter, Depends, HTTPException
from data.schemas import ProfessionalRegistration,ProfessionalBase
from services import professional_services
from data.database import get_db
from sqlalchemy.orm import Session

professionals_router = APIRouter(prefix='/professionals')


@professionals_router.post('/register', response_model=ProfessionalBase)
def register(user: ProfessionalRegistration, db: Session = Depends(get_db)):
    db_user = professional_services.get_pro_by_username(db, username=user.Username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return professional_services.register(user=user, db=db)

@professionals_router.get('/{id}')
def get_personal_info(id: int):
    pass


@professionals_router.put('/{id}')
def edit_personal_info(id: int):
    pass


@professionals_router.post('/{id}/ad')
def create_ad():
    pass


@professionals_router.get('/{id}/ads')
def get_all_ads(id: int):
    # Will include options to search/filter the ads
    pass


@professionals_router.get('/{id}/{ad_id}')
def get_ad(id: int, ad_id: int):
    # Check if the ad exists first
    pass

@professionals_router.put('/{id}/{ad_id}')
def edit_ad(id: int, ad_id: int):
    # Check if the ad exists first
    pass


@professionals_router.patch('/{id}/{ad_id}')
def set_main_ad(id: int, ad_id: int):
    # Maybe first check if there is not already set main ad
    pass












