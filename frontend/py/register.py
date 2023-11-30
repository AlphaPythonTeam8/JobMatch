from fastapi import APIRouter, Response, Query, FastAPI, Form
from frontend.py.services import check_username_exist, create_company, create_professional, check_username_exist_professional
from fastapi import APIRouter, Response, Query, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext



register_router = APIRouter(prefix='/users')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(password: str):
    return bcrypt_context.hash(password)


@register_router.post('/company', tags=["Garbage"])
def register_company(username: str = Form(),
             company_name: str = Form(),
             email: str = Form(),
             password: str = Form(),
             ):
    hashed_password = hash_password(password)

    if check_username_exist(username):
        return Response(status_code=400, content=f'Username is already taken!')
    else:
        user = create_company(username, company_name, email, hashed_password)
        return user



@register_router.post('/professional', tags=["Garbage"])
def register_professional(username: str = Form(),
             first_name: str = Form(),
             last_name: str = Form(),
             professional_email: str = Form(),
             password: str = Form()
             ):
    hashed_password = hash_password(password)

    if check_username_exist_professional(username):
        return Response(status_code=400, content=f'Username is already taken!')
    else:
        user = create_professional(username, first_name, last_name, professional_email, hashed_password)
        return user