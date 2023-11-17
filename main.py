from fastapi import FastAPI

from routers.companies import companies_router
from routers.professionals import professionals_router

app = FastAPI()

app.include_router(professionals_router)
app.include_router(companies_router)
