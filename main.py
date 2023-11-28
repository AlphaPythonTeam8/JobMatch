import uvicorn
from fastapi import FastAPI

from common.auth import auth_router, professional_auth_router
from routers.companies import companies_router
from routers.jobad import job_ad_router
from routers.professionals import professionals_router
from routers.searching import searching_router

app = FastAPI()

app.include_router(professionals_router)
app.include_router(companies_router)
app.include_router(auth_router)
app.include_router(professional_auth_router)
app.include_router(searching_router)
app.include_router(job_ad_router)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)

#
# {
#   "Username": "ABV202",
#   "CompanyName": "ABVC",
#   "Email": "abvc@abv.bg",
#   "Password": "Aa12@!vx",
#   "VerificationToken": "string",
#   "EmailVerified": false
# }
