import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock, Mock
import data.schemas as s


def fake_company(
        Username="ABV20",
        CompanyName="ABV",
        Email="abv@abv.bg",
        Password="aAbB12!!",
        VerificationToken="kx2IglpWl7QpABl",
        EmailVerified=False):
    mock_company_registration = MagicMock(spec=s.CompanyRegistration)
    mock_company_registration.Username = Username
    mock_company_registration.CompanyName = CompanyName
    mock_company_registration.Email = Email
    mock_company_registration.Password = Password
    mock_company_registration.VerificationToken = VerificationToken
    mock_company_registration.EmailVerified = EmailVerified

    return mock_company_registration


def fake_professional(ProfessionalID=1,
                      Username='test1',
                      FirstName='Test',
                      LastName='Testov',
                      ProfessinalEmail='test1@test.com',
                      Password='test111',
                      BriefSummary=None,
                      Location=None,
                      Status=None,
                      PhotoURL=None,
                      CVURL=None,
                      Contact=None,
                      ):
    mock_professional_registration = MagicMock()
    mock_professional_registration.ProfessionalID = ProfessionalID
    mock_professional_registration.Username = Username
    mock_professional_registration.FirstName = FirstName
    mock_professional_registration.LastName = LastName
    mock_professional_registration.ProfessionalEmail = ProfessinalEmail
    mock_professional_registration.Password = Password
    mock_professional_registration.BriefSummary = BriefSummary
    mock_professional_registration.Location = Location
    mock_professional_registration.Status = Status
    mock_professional_registration.PhotoURL = PhotoURL
    mock_professional_registration.CVURL = CVURL
    mock_professional_registration.Contact = Contact
    return mock_professional_registration


def fake_professional_updated(Username='test1',
                              FirstName='Test',
                              LastName='Testov',
                              ProfessionalEmail='test1@test.com',
                              BriefSummary='Developer',
                              Location='Sofia',
                              Status='Active',
                              PhotoURL=None,
                              CVURL=None,
                              Contact='088818181',
                              ActiveAds=3,
                              ):
    mock_professional = MagicMock(spec=s.ProfessionalResponse)
    mock_professional.Username = Username
    mock_professional.FirstName = FirstName
    mock_professional.LastName = LastName
    mock_professional.ProfessionalEmail = ProfessionalEmail
    mock_professional.BriefSummary = BriefSummary
    mock_professional.Location = Location
    mock_professional.Status = Status
    mock_professional.PhotoURL = PhotoURL
    mock_professional.CVURL = CVURL
    mock_professional.Contact = Contact
    mock_professional.ActiveAds = ActiveAds
    return mock_professional


def fake_match_request(CompanyName='Test',
                       MatchStatus='Pending',
                       SentAt='2023, 12, 1, 10, 0, 0'):
    mock_request = MagicMock(spec=s.CompanyAdMatchRequest)
    mock_request.CompanyName = CompanyName
    mock_request.MatchStatus = MatchStatus
    mock_request.SentAt = SentAt
    return mock_request


def fake_company_ad(
        CompanyAdID=1,
        ProfessionalID=1,
        FirstName='Test',
        LastName='Testov',
        BottomSalary='1500',
        TopSalary='2000',
        MotivationDescription='Developer',
        Location='Sofia',
        Skills=list,
        Status='Active',
        CompanyAdRequirement=None,
        CreatedAt=datetime(2023, 12, 1, 10, 0, 0),
        UpdatedAt=datetime(2023, 12, 1, 10, 30, 0),
        MatchRequests=list):
    mock_company_ad = MagicMock(spec=s.CompanyAdResponse)
    mock_company_ad.CompanyAdID = CompanyAdID
    mock_company_ad.ProfessionalID = ProfessionalID
    mock_company_ad.FirstName = FirstName
    mock_company_ad.LastName = LastName
    mock_company_ad.BottomSalary = BottomSalary
    mock_company_ad.TopSalary = TopSalary
    mock_company_ad.MotivationDescription = MotivationDescription
    mock_company_ad.Location = Location
    mock_company_ad.Status = Status
    mock_company_ad.Skills = Skills
    mock_company_ad.CompanyAdRequirement = CompanyAdRequirement
    mock_company_ad.CreatedAt = CreatedAt
    mock_company_ad.UpdatedAt = UpdatedAt
    mock_company_ad.MatchRequests = MatchRequests
    return mock_company_ad



def fake_response(exact_response, content, status_code=0):
    mock_response = Mock(spec=exact_response)
    mock_response.status_code = status_code
    mock_response.content = content
    return mock_response