import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock, Mock
import data.schemas as s
from data.models import Admin


def fake_company(
        Username="ABV20",
        CompanyName="ABV",
        Email="abv@abv.bg",
        Password="aAbB12!!",
        VerificationToken="kx2IglpWl7QpABl",
        EmailVerified=False,
        IsBlocked=False):
    mock_company = MagicMock(spec=s.Company)
    mock_company.Username = Username
    mock_company.CompanyName = CompanyName
    mock_company.Email = Email
    mock_company.Password = Password
    mock_company.VerificationToken = VerificationToken
    mock_company.EmailVerified = EmailVerified
    mock_company.IsBlocked = IsBlocked
    return mock_company

def fake_company_updated(
        Username='ABV20',
        CompanyName='ABV',
        Email='abv@abv.bg',
        Description='A leading company in the industry',
        Location='New York',
        PictureURL='http://example.com/company.jpg',
        Contact='contact@abv.bg',
        ActiveAds=5,
        IsBlocked=False):
    mock_company = MagicMock(spec=s.CompanyResponse)
    mock_company.Username = Username
    mock_company.CompanyName = CompanyName
    mock_company.Email = Email
    mock_company.Description = Description
    mock_company.Location = Location
    mock_company.PictureURL = PictureURL
    mock_company.Contact = Contact
    mock_company.ActiveAds = ActiveAds
    mock_company.IsBlocked = IsBlocked
    return mock_company
def fake_professional(
        ProfessionalID=1,
        Username='test1',
        FirstName='Test',
        LastName='Testov',
        ProfessionalEmail='test1@test.com',
        Password='test111',
        BriefSummary=None,
        Location=None,
        Status=None,
        PhotoURL=None,
        CVURL=None,
        Contact=None,
        IsBlocked=False):
    mock_professional = MagicMock(spec=s.Professional)
    mock_professional.ProfessionalID = ProfessionalID
    mock_professional.Username = Username
    mock_professional.FirstName = FirstName
    mock_professional.LastName = LastName
    mock_professional.ProfessionalEmail = ProfessionalEmail
    mock_professional.Password = Password
    mock_professional.BriefSummary = BriefSummary
    mock_professional.Location = Location
    mock_professional.Status = Status
    mock_professional.PhotoURL = PhotoURL
    mock_professional.CVURL = CVURL
    mock_professional.Contact = Contact
    mock_professional.IsBlocked = IsBlocked
    return mock_professional


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


def fake_job_ad(
        JobAdID=1,
        ProfessionalID=1,
        FirstName='Test',
        LastName='Testov',
        BottomSalary='1500',
        TopSalary='2000',
        MotivationDescription='Developer',
        Location='Sofia',
        Skills=list,
        Status='Active',
        JobAdRequirement=None,
        CreatedAt=datetime(2023, 12, 1, 10, 0, 0),
        UpdatedAt=datetime(2023, 12, 1, 10, 30, 0),
        MatchRequests=list):
    mock_job_ad = MagicMock(spec=s.JobAdResponse)
    mock_job_ad.JobAdID = JobAdID
    mock_job_ad.ProfessionalID = ProfessionalID
    mock_job_ad.FirstName = FirstName
    mock_job_ad.LastName = LastName
    mock_job_ad.BottomSalary = BottomSalary
    mock_job_ad.TopSalary = TopSalary
    mock_job_ad.MotivationDescription = MotivationDescription
    mock_job_ad.Location = Location
    mock_job_ad.Status = Status
    mock_job_ad.Skills = Skills
    mock_job_ad.JobAdRequirement = JobAdRequirement
    mock_job_ad.CreatedAt = CreatedAt
    mock_job_ad.UpdatedAt = UpdatedAt
    mock_job_ad.MatchRequests = MatchRequests
    return mock_job_ad


def fake_response(exact_response, content, status_code=0):
    mock_response = Mock(spec=exact_response)
    mock_response.status_code = status_code
    mock_response.content = content
    return mock_response


def fake_admin(AdminID=1, Username="adminUser", Password="securePassword!"):
    mock_admin = MagicMock(spec=Admin)
    mock_admin.AdminID = AdminID
    mock_admin.Username = Username
    mock_admin.Password = Password
    return mock_admin
