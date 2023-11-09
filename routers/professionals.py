from fastapi import APIRouter

professionals_router = APIRouter(prefix='/professionals')


@professionals_router.post('/register')
def register():
    pass


@professionals_router.get('/{id}')
def get_personal_info(id: int):
    pass


@professionals_router.post('/{id}')
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
def get_ad(professional_id: int, ad_id: int):
    # Check if the ad exists first
    pass

@professionals_router.post('/{id}/{ad_id}')
def edit_ad(professional_id: int, ad_id: int):
    # Check if the ad exists first
    pass


@professionals_router.patch('/{id}/{ad_id}')
def set_main_ad(professional_id: int, ad_id: int):
    # Maybe first check if there is not already set main ad
    pass












