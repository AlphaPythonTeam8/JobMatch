import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict, HttpUrl


class ProfessionalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Username: str = Field(pattern=r'^\w{2,30}$')
    FirstName: str = Field(pattern=r'^[a-zA-Z]{2,30}$')
    LastName: str = Field(pattern=r'^[a-zA-Z]{2,30}$')


class ProfessionalRegistration(ProfessionalBase):
    Password: str

    @field_validator('Password')
    @classmethod
    def validate_password(cls, password: str):
        pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
        if re.match(pattern, password):
            return password
        else:
            raise ValueError('Password not strong enough')


class Professional(ProfessionalBase):  # TODO - Add the photo
    BriefSummary: str | None
    Location: str | None
    Status: str
    Contact: str | None


class CompanyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Username: str = Field(pattern=r'^\w{2,30}$')
    CompanyName: str = Field(pattern=r'^[a-zA-Z]{2,30}$')


class CompanyRegistration(CompanyBase):
    Password: str

    @field_validator('Password')
    @classmethod
    def validate_password(cls, password: str):
        pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
        if re.match(pattern, password):
            return password
        else:
            raise ValueError('Password not strong enough')


class Company(CompanyBase):
    Description: str | None
    Location: str | None = Field(None, min_length=5, max_length=255)
    PictureURL: HttpUrl | None
    Contact: str | None = Field(None, min_length=5, max_length=255)


class CompanyLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class CompanyAd(BaseModel):
    SalaryRange: str
    MotivationDescription: str
    Location: str
    Status: str | None = None
    Skills: str
    CompanyAdRequirement: str | None = None


class JobAd:
    SalaryRange: str
    JobDescription: str
    Location: str
    Status: str | None = None
    JobRequirement: str
    Skills: str
    CreatedAt: datetime = None
    UpdatedAt: datetime = None


class JobAdResponse(BaseModel):
    JobAdID: int
    CreatedAt: datetime
