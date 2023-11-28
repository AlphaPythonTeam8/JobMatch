import unittest
from unittest.mock import patch, MagicMock
from data.schemas import CompanyRegistration


def fake_company(
                 Username="ABV20",
                 CompanyName="ABV",
                 Email="abv@abv.bg",
                 Password="aAbB12!!",
                 VerificationToken="kx2IglpWl7QpABl",
                 EmailVerified=False):
    mock_company_registration = MagicMock(spec=CompanyRegistration)
    mock_company_registration.Username = Username
    mock_company_registration.CompanyName = CompanyName
    mock_company_registration.Email = Email
    mock_company_registration.Password = Password
    mock_company_registration.VerificationToken = VerificationToken
    mock_company_registration.EmailVerified = EmailVerified

    return mock_company_registration
