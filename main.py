import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from common.auth import auth_router, professional_auth_router, admin_auth_router
from routers.companies import companies_router
from routers.jobad import job_ad_router
from routers.matches import matches_router
from routers.professionals import professionals_router
from routers.searching import searching_router
from frontend.py.register import register_router
from routers.admin import admin_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(professionals_router)
app.include_router(admin_router)
app.include_router(companies_router)
app.include_router(auth_router)
app.include_router(professional_auth_router)
app.include_router(admin_auth_router)
app.include_router(searching_router)
app.include_router(job_ad_router)
app.include_router(matches_router)
app.include_router(register_router)

add_pagination(app)


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)

#
# {
#   "Username": "ABV202",
#   "CompanyName": "ABVC",
#   "Email": "abvc@abv.bg",
#   "Password": "Ba12@!vx",
#   "VerificationToken": "string",
#   "EmailVerified": false
# }


{
  "Username": "SBN20",
  "FirstName": "Suzu",
  "LastName": "Goru",
  "ProfessionalEmail": "suzugoru@example.com",
  "Password": "S2fgG#21!"
}