import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict, HttpUrl, EmailStr, validator

from data.models import Skill


class ProfessionalBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Username: str = Field(pattern=r'^\w{2,30}$')
    FirstName: str = Field(pattern=r'^[a-zA-Z]{2,30}$')
    LastName: str = Field(pattern=r'^[a-zA-Z]{2,30}$')
    ProfessionalEmail: EmailStr

    @field_validator('ProfessionalEmail')
    @classmethod
    def validate_email(cls, email: str):
        pattern = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.match(pattern, email):
            return email
        else:
            raise ValueError('Email format is incorrect.')


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


class Professional(ProfessionalBase):
    BriefSummary: str | None = Field(min_length=5, max_length=255)
    Location: str | None = Field(min_length=2, max_length=50)
    Status: str | None
    Contact: str | None = Field(min_length=5, max_length=100)

class ProfessionalResponse(Professional):
    ActiveAds: int
    PhotoURL: str | None
    CVURL: str | None


class CompanyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Username: str = Field(pattern=r'^\w{2,30}$')
    CompanyName: str = Field(pattern=r'^[a-zA-Z]{2,30}$')
    Email: EmailStr

    @field_validator('Email')
    @classmethod
    def validate_email(cls, email: str):
        pattern = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.match(pattern, email):
            return email
        else:
            raise ValueError('Email format is incorrect.')

class Company(CompanyBase):
    Description: str | None
    Location: str | None = Field(None, min_length=5, max_length=255)
    PictureURL: str | None
    Contact: str | None = Field(None, min_length=5, max_length=255)

class CompanyRegistration(CompanyBase):
    Password: str
    VerificationToken: str
    EmailVerified: bool = False

    @field_validator('Password')
    @classmethod
    def validate_password(cls, password: str):
        pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
        if re.match(pattern, password):
            return password
        else:
            raise ValueError('Password not strong enough')


class CompanyResponse(Company):
    ActiveAds : int


class CompanyLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class CompanyAd(BaseModel):
    BottomSalary: int | None
    TopSalary: int | None
    MotivationDescription: str
    Location: str
    Status: str | None = None
    Skills: str | list
    CompanyAdRequirement: str | None = None


class CompanyAdsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    BottomSalary: int | None
    TopSalary: int | None
    MotivationDescription: str
    Location: str
    Skills: list
    Status: str | None
    CompanyAdRequirement: str | None
    CreatedAt: datetime
    UpdatedAt: datetime

class CompanyAdsResponse2(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    CompanyAdID: Optional[int]
    BottomSalary: int | None
    TopSalary: int | None
    MotivationDescription: str
    Location: str
    Skills: list
    Status: str | None
    CompanyAdRequirement: str | None
    CreatedAt: datetime
    UpdatedAt: datetime


class CompanyAdMatchRequest(BaseModel):
    CompanyName: str
    MatchStatus: str
    SentAt: datetime


class CompanyAdResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    FirstName: str
    LastName: str
    BottomSalary: int | None
    TopSalary: int | None
    MotivationDescription: str
    Location: str
    Skills: list
    Status: str
    CompanyAdRequirement: str | None
    CreatedAt: datetime
    UpdatedAt: datetime


class CompanyAdResponseMatch(CompanyAdResponse):
    MatchRequests: list

class JobAd(BaseModel):
    BottomSalary: int | None
    TopSalary: int | None
    JobDescription: str
    Location: str
    Status: str | None = None
    Skills: str


# class JobAdResponse(JobAd):
#     JobAdID: int
#     CreatedAt: datetime = None
#     UpdatedAt: datetime = None
class JobAdResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    BottomSalary: int | None
    TopSalary: int | None
    JobDescription: str
    Location: str
    Status: str
    Skills: list
    CreatedAt: datetime
    UpdatedAt: datetime

class JobAdResponse2(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    JobAdID: int
    BottomSalary: int | None
    TopSalary: int | None
    JobDescription: str
    Location: str
    Status: str
    Skills: list
    CreatedAt: datetime
    UpdatedAt: datetime



class ProfessionalUpdate(BaseModel):
    BriefSummary: str | None = Field(min_length=5, max_length=255, default=None)
    Location: str | None = Field(min_length=2, max_length=50, default=None)
    Status: str | None = 'Active'
    PhotoURL: str | None = None
    CVURL: str | None = None
    Contact: str | None = Field(min_length=5, max_length=100, default=None)


class CompanyUpdate(BaseModel):
    Description: str | None = Field(min_length=5, max_length=255, default=None)
    Location: str | None = Field(min_length=2, max_length=50, default=None)
    PictureURL: str | None = None
    Contact: str | None = Field(min_length=5, max_length=255, default=None)



class JobAdUpdate(BaseModel):
    BottomSalary: Optional[int]
    TopSalary: Optional[int]
    JobDescription: Optional[str]
    Location: Optional[str]
    Status: Optional[str]
    Skills: str | list

class ChangePassword(BaseModel):
    new_password: str
    confirm_new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, password: str):
        pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
        if re.match(pattern, password):
            return password
        else:
            raise ValueError('New password not strong enough')

    @validator('confirm_new_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
