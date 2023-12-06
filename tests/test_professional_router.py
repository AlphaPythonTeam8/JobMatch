from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch
import data_test as dt
from sqlalchemy.orm import Session
from data import schemas as s
from routers import professionals
from fastapi import HTTPException, Response
from fastapi_pagination import LimitOffsetPage, paginate, add_pagination


class Professionals_Should(TestCase):

    def test_get_personal_info_returnProfessional(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_pro') as mock_get_pro:
            mock_session = Mock(spec=Session)
            mock_professional = dt.fake_professional()
            mock_get_db.return_value = mock_session
            mock_response = s.ProfessionalResponse(
                Username=mock_professional.Username,
                FirstName=mock_professional.FirstName,
                LastName=mock_professional.LastName,
                ProfessionalEmail=mock_professional.ProfessionalEmail,
                BriefSummary=mock_professional.BriefSummary,
                Location=mock_professional.Location,
                Status=mock_professional.Status,
                Contact=mock_professional.Contact,
                ActiveAds=3,
                PhotoURL=mock_professional.PhotoURL,
                CVURL=mock_professional.CVURL
            )

            mock_get_professional.return_value = s.TokenData(id=1)
            mock_get_pro.return_value = mock_response

            result = professionals.get_personal_info(mock_get_professional, mock_session)

            self.assertEqual(mock_response, result)
            self.assertEqual(mock_professional.FirstName, result.FirstName)
            self.assertEqual(mock_professional.LastName, result.LastName)
            mock_get_pro.assert_called_once()

    def test_get_ad_returnCompanyAd(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad, \
                patch('services.professional_services.return_ad') as mock_return_ad:
            mock_session = Mock(spec=Session)
            mock_company_ad = dt.fake_company_ad()
            mock_get_ad.return_value = mock_company_ad
            mock_return_ad.return_value = mock_company_ad
            mock_get_db.return_value = mock_session

            result = professionals.get_ad(1, s.TokenData(id=1), mock_session)

            self.assertEqual(mock_company_ad, result)
            self.assertEqual(mock_company_ad.BottomSalary, result.BottomSalary)
            self.assertEqual(mock_company_ad.Location, result.Location)
            mock_get_ad.assert_called_once()
            mock_return_ad.assert_called_once()

    def test_get_ad_returnNotFound_whenAdDoesNotExist(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_get_ad.return_value = None
            mock_get_professional.return_value = s.TokenData(id=1)

            with self.assertRaises(HTTPException) as context:
                professionals.get_ad(1, mock_get_professional, mock_session)

            raised_exception = context.exception

            self.assertEqual(404, raised_exception.status_code)
            self.assertEqual(context.exception.detail, raised_exception.detail)

    def test_get_ad_returnForbidden_whenAdDoesNotBelongToUser(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_get_ad.return_value = dt.fake_company_ad(ProfessionalID=2)
            mock_get_professional.return_value = s.TokenData(id=1)

            with self.assertRaises(HTTPException) as context:
                professionals.get_ad(1, mock_get_professional, mock_session)

            raised_exception = context.exception

            self.assertEqual(403, raised_exception.status_code)
            self.assertEqual(context.exception.detail, raised_exception.detail)

    def test_edit_ad_returnCompanyAd(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad, \
                patch('services.professional_services.edit_ad') as mock_edit_ad:
            old_ad = dt.fake_company_ad()
            new_ad = s.CompanyAd(BottomSalary='1600',
                                 TopSalary='2100',
                                 MotivationDescription='Junior Developer',
                                 Location='Sofia',
                                 Skills='Python - Advanced')
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_get_ad.return_value = old_ad

            expected = s.CompanyAdResponse(
                FirstName=old_ad.FirstName,
                LastName=old_ad.LastName,
                BottomSalary=new_ad.BottomSalary,
                TopSalary=new_ad.TopSalary,
                MotivationDescription=new_ad.MotivationDescription,
                Location=new_ad.Location,
                Status=old_ad.Status,
                Skills=['Python - Advanced'],
                CompanyAdRequirement=old_ad.CompanyAdRequirement,
                CreatedAt=old_ad.CreatedAt,
                UpdatedAt=old_ad.UpdatedAt
            )

            mock_edit_ad.return_value = expected

            result = professionals.edit_ad(new_ad, 1, s.TokenData(id=1), mock_session)

            self.assertEqual(expected, result)
            self.assertEqual(expected.BottomSalary, result.BottomSalary)
            self.assertEqual(expected.Location, result.Location)
            mock_get_ad.assert_called_once()
            mock_edit_ad.assert_called_once()

    def test_edit_ad_returnNotFound_WhenAdDoesNotExists(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_get_professional.return_value = s.TokenData(id=1)
            mock_get_ad.return_value = None
            new_ad = s.CompanyAd(BottomSalary='1600',
                                 TopSalary='2100',
                                 MotivationDescription='Junior Developer',
                                 Location='Sofia',
                                 Skills='Python - Advanced')

            with self.assertRaises(HTTPException) as context:
                professionals.edit_ad(new_ad, 1, mock_get_professional, mock_session)

            raised_exception = context.exception

            self.assertEqual(404, raised_exception.status_code)
            self.assertEqual(context.exception.detail, raised_exception.detail)

    def test_edit_ad_returnForbidden_WhenAdDoesNotBelongToUser(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_get_professional.return_value = s.TokenData(id=1)
            new_ad = s.CompanyAd(BottomSalary='1600',
                                 TopSalary='2100',
                                 MotivationDescription='Junior Developer',
                                 Location='Sofia',
                                 Skills='Python - Advanced')
            mock_get_ad.return_value = dt.fake_company_ad(ProfessionalID=2)

            with self.assertRaises(HTTPException) as context:
                professionals.edit_ad(new_ad, 1, s.TokenData(id=1), mock_session)

            raised_exception = context.exception

            self.assertEqual(403, raised_exception.status_code)
            self.assertEqual(context.exception.detail, raised_exception.detail)

    def test_set_main_ad_returnOK(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad, \
                patch('services.professional_services.set_main_ad') as mock_set_main_ad:
            mock_company_ad = dt.fake_company_ad()
            mock_get_ad.return_value = mock_company_ad
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session

            expected = Response(status_code=200, content='Main company ad was set.')

            mock_set_main_ad.return_value = expected

            result = professionals.set_main_ad(1, s.TokenData(id=1), mock_session)

            self.assertEqual(expected.status_code, result.status_code)

    def test_set_main_ad_returnNotFound_whenNoAdOrDoesNotBelongToUser(self):
        with patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_ad') as mock_get_ad:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_get_ad.return_value = None
            mock_get_professional.return_value.id = 1

            with self.assertRaises(HTTPException) as context:
                professionals.set_main_ad(1, mock_get_professional, mock_session)

            raised_exception = context.exception

            self.assertEqual(404, raised_exception.status_code)
            self.assertEqual(context.exception.detail, raised_exception.detail)

    def test_register_returnProfessionalBase(self):
        with patch('data.database.get_db') as mock_get_db, \
                patch('common.hashing.hash_password') as mock_hash_password, \
                patch('services.professional_services.get_pro_by_username') as mock_get_pro, \
                patch('services.professional_services.register') as mock_register, \
                patch('services.professional_services.email_exists') as mock_email_exists:
            mock_session = Mock(spec=Session)
            mock_professional = dt.fake_professional()
            user_registration = s.ProfessionalRegistration(
                Username=mock_professional.Username,
                FirstName=mock_professional.FirstName,
                LastName=mock_professional.LastName,
                ProfessionalEmail=mock_professional.ProfessionalEmail,
                Password='Test111!'
            )
            mock_hash_password.return_value = 'Test111!'
            mock_get_db.return_value = mock_session
            mock_get_pro.return_value = None
            mock_email_exists.return_value = None

            expected = s.ProfessionalBase(
                Username=mock_professional.Username,
                FirstName=mock_professional.FirstName,
                LastName=mock_professional.LastName,
                ProfessionalEmail=mock_professional.ProfessionalEmail
            )

            mock_register.return_value = expected

            result = professionals.register(user_registration, mock_session)

            self.assertEqual(expected, result)
            mock_get_pro.assert_called_once()
            mock_register.assert_called_once()
            mock_email_exists.assert_called_once()

    def test_register_returnBadRequest_WhenUsernameAlreadyTaken(self):
        with patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.get_pro_by_username') as mock_get_pro:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_professional = dt.fake_professional()
            user_registration = s.ProfessionalRegistration(
                Username=mock_professional.Username,
                FirstName=mock_professional.FirstName,
                LastName=mock_professional.LastName,
                ProfessionalEmail=mock_professional.ProfessionalEmail,
                Password='Test111!'
            )

            mock_get_pro.return_value = mock_professional

            with self.assertRaises(HTTPException) as context:
                professionals.register(user_registration, mock_session)

            raised_exception = context.exception

            self.assertEqual(400, raised_exception.status_code)
            self.assertEqual(context.exception.detail, raised_exception.detail)

    def test_register_returnBadRequest_WhenEmailAlreadyTaken(self):
        with patch('data.database.get_db') as mock_get_db, \
                patch('services.professional_services.email_exists') as mock_email_exists:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_professional = dt.fake_professional()
            user_registration = s.ProfessionalRegistration(
                Username=mock_professional.Username,
                FirstName=mock_professional.FirstName,
                LastName=mock_professional.LastName,
                ProfessionalEmail=mock_professional.ProfessionalEmail,
                Password='Test111!'
            )

            mock_email_exists.return_value = mock_professional

            with self.assertRaises(HTTPException) as context:
                professionals.register(user_registration, mock_session)

            raised_exception = context.exception

            self.assertEqual(400, raised_exception.status_code)
            self.assertEqual(context.exception.detail, raised_exception.detail)

    def test_create_ad_returnCompanyAd(self):
        with patch('data.database.get_db') as mock_get_db, \
                patch('common.oauth2.get_current_professional') as mock_get_professional, \
                patch('services.professional_services.add_skills_to_db') as mock_add_skills,\
                patch('services.professional_services.create_ad') as mock_create_ad:
            mock_session = Mock(spec=Session)
            mock_get_db.return_value = mock_session
            mock_ad = dt.fake_company_ad()
            mock_get_professional.return_value.id = 1

            expected = s.CompanyAdResponse(
                FirstName=mock_ad.FirstName,
                LastName=mock_ad.LastName,
                BottomSalary=mock_ad.BottomSalary,
                TopSalary=mock_ad.TopSalary,
                MotivationDescription=mock_ad.MotivationDescription,
                Location=mock_ad.Location,
                Skills=['Python - advanced'],
                Status=mock_ad.Status,
                CreatedAt=mock_ad.CreatedAt,
                UpdatedAt=mock_ad.UpdatedAt,
                CompanyAdRequirement=mock_ad.CompanyAdRequirement
            )

            mock_create_ad.return_value = expected

            result = professionals.create_ad(
                bottom_salary=mock_ad.BottomSalary,
                top_salary=mock_ad.TopSalary,
                motivation_description=mock_ad.MotivationDescription,
                location=mock_ad.Location,
                status=mock_ad.Status,
                skills='Python - advanced',
                company_ad_requirement=mock_ad.CompanyAdRequirement,
                user_id=mock_get_professional, db=mock_session
            )

            self.assertEqual(expected, result)


    # def test_get_all_ads_SortedAscending(self):
    #     with patch('data.database.get_db') as mock_get_db, \
    #             patch('common.oauth2.get_current_professional') as mock_get_professional, \
    #             patch('services.professional_services.get_all_ads') as mock_get_all_ads:
    #         mock_session = Mock(spec=Session)
    #         mock_get_db.return_value = mock_session
    #         mock_get_professional.return_value.id = 1
    #
    #         mock_ad_1 = dt.fake_company_ad()
    #         mock_ad_2 = dt.fake_company_ad(UpdatedAt=datetime(2023, 11, 30, 6, 0, 0))
    #
    #         expected = [mock_ad_2, mock_ad_1]
    #
    #         mock_get_all_ads.return_value = expected
    #
    #         result = professionals.get_all_ads(sort='asc', user_id=mock_get_professional, db=mock_session)
    #
    #         assert isinstance(result, LimitOffsetPage)
    #         assert len(expected) == result.total
    #         assert expected == result.items
