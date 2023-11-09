from fastapi import APIRouter

companies_router = APIRouter(prefix='/companies')


@companies_router.post('/')
def register():
    pass


@companies_router.get('/{id}')
def get_info(id: int):
    pass


@companies_router.put('/{id}')
def edit_info(id: int):
    pass


@companies_router.post('/{id}')
def create_ad(id: int):
    pass


@companies_router.get('/{id}/{ad_id}')
def get_ad(id: int, ad_id: int):
    pass


@companies_router.put('/{id}/{ad_id}')
def edit_add(id: int, ad_id: int):
    pass