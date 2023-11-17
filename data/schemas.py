import re
from pydantic import BaseModel, Field, field_validator, ConfigDict


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


class Professional(ProfessionalBase): #TODO - Add the photo
    BriefSummary: str | None
    Location: str | None
    Status: str
    Contact: str | None