import unittest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, call
import data.schemas as s
import data.models as m
import data_test as dt
from services import professional_services
from sqlalchemy.orm import Session
import sqlalchemy.exc


class ProfessionalServices_Should(unittest.TestCase):
    def test_register(self):
        db = Mock(spec=Session)
        mock_professional = dt.fake_professional()
        result = professional_services.register(mock_professional, db)

        self.assertEqual(mock_professional.FirstName, result.FirstName)
        self.assertEqual(mock_professional.Username, result.Username)
        self.assertEqual(mock_professional.LastName, result.LastName)
        self.assertEqual(mock_professional.ProfessionalEmail, result.ProfessionalEmail)
        self.assertEqual(mock_professional.Password, result.Password)

    def test_email_exists_returns_Professional_WhenEmailExists(self):
        mock_session = Mock(spec=Session)
        mock_professional = dt.fake_professional()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_professional
        result = professional_services.email_exists(mock_session, 'test1@test.com')
        self.assertEqual(mock_professional, result)
        mock_session.query.assert_called_once_with(m.Professional)

    def test_email_exists_returns_None_WhenEmailNotFound(self):
        mock_session = Mock(spec=Session)
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = professional_services.email_exists(mock_session, 'test1@test.com')
        self.assertIsNone(result)

    def test_get_pro_returns_ProfessionalResponse(self):
        with patch('data.models.CompanyAd', spec=True) as mock_company_ad, \
                patch('data.models.Professional', spec=True) as mock_professional:
            mock_session = MagicMock(spec=Session)
            mock_profile = dt.fake_professional()

            mock_session.query.return_value.filter.return_value.first.return_value = mock_profile
            mock_session.query.return_value.filter.return_value.count.return_value = 1

            expected = s.ProfessionalResponse(
                Username=mock_profile.Username,
                FirstName=mock_profile.FirstName,
                LastName=mock_profile.LastName,
                ProfessionalEmail=mock_profile.ProfessionalEmail,
                BriefSummary=None,
                Location=None,
                Status=None,
                PhotoURL=None,
                CVURL=None,
                Contact=None,
                ActiveAds=1
            )

            result = professional_services.get_pro(1, mock_session)

            self.assertEqual(expected.FirstName, result.FirstName)
            self.assertEqual(expected.LastName, result.LastName)
            self.assertEqual(expected.Username, result.Username)
            self.assertEqual(expected.ProfessionalEmail, result.ProfessionalEmail)
            self.assertEqual(expected.BriefSummary, result.BriefSummary)
            self.assertEqual(expected.Location, result.Location)
            self.assertEqual(expected.Status, result.Status)
            self.assertEqual(expected.PhotoURL, result.PhotoURL)
            self.assertEqual(expected.CVURL, result.CVURL)
            self.assertEqual(expected.Contact, result.Contact)
            self.assertEqual(expected.ActiveAds, 1)

            mock_session.query.return_value.filter.return_value.first.assert_called_once()
            mock_session.query.return_value.filter.return_value.count.assert_called_once()

    def test_get_names(self):
        mock_session = Mock(spec=Session)
        mock_session.query.return_value.filter.return_value.first.return_value = ('Test', 'Testov')
        result = professional_services.get_names(1, mock_session)

        self.assertEqual(('Test', 'Testov'), result)

    def test_get_pro_by_username_returnProfessional_whenFound(self):
        mock_session = Mock(spec=Session)
        mock_professional = dt.fake_professional()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_professional
        result = professional_services.get_pro_by_username(mock_session, 'test1')

        self.assertEqual(mock_professional, result)
        mock_session.query.assert_called_once_with(m.Professional)

    def test_get_pro_by_username_returnNone_whenNotFound(self):
        mock_session = Mock(spec=Session)
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = professional_services.get_pro_by_username(mock_session, 'test2')

        self.assertIsNone(result)

    def test_update_info_Successfully_returnProfessionalResponse(self):
        with patch('data.models.Professional', spec=True) as mock_professional:
            mock_session = Mock(spec=Session)
            mock_profile = dt.fake_professional()
            mock_session.query.return_value.filter.return_value = mock_profile
            mock_session.query.return_value.filter.return_value.first.return_value = dt.fake_professional_updated()
            mock_session.query.return_value.filter.return_value.count.return_value = 3

            update_profile = s.ProfessionalUpdate(
                BriefSummary='Developer',
                Location='Sofia',
                Status='Active',
                PhotoURL=None,
                CVURL=None,
                Contact='088818181'
            )

            expected = s.ProfessionalResponse(
                Username='test1',
                FirstName='Test',
                LastName='Testov',
                ProfessionalEmail='test1@test.com',
                BriefSummary=update_profile.BriefSummary,
                Location=update_profile.Location,
                Status=update_profile.Status,
                PhotoURL=None,
                CVURL=None,
                Contact=update_profile.Contact,
                ActiveAds=3
            )
            result = professional_services.update_info(1, update_profile, mock_session)

            self.assertEqual(expected, result)

    def test_get_match_requests_for_ad_returnMatchRequests_whenFound(self):
        with patch('data.models.Match') as mock_match:
            mock_session = Mock(spec=Session)
            match_1 = dt.fake_match_request()
            match_2 = dt.fake_match_request('Test2', 'Pending', '2023, 12, 2, 11, 0, 0')
            mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = (match_1, match_2)
            result = professional_services.get_match_requests_for_ad(1, mock_session)

            self.assertEqual((match_1, match_2), result)
            self.assertEqual(2, len(result))
            mock_session.query.return_value.join.return_value.filter.return_value.all.assert_called_once()
            mock_session.query.return_value.join.return_value.filter.assert_called_once_with(
                m.Match.CompanyAdID == 1)

    def test_get_match_requests_for_ad_returnNone_whenNotFound(self):
        with patch('data.models.Match') as mock_match:
            mock_session = Mock(spec=Session)
            mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = None
            result = professional_services.get_match_requests_for_ad(1, mock_session)

            self.assertIsNone(result)
            mock_session.query.return_value.join.return_value.filter.assert_called_once_with(
                m.Match.CompanyAdID == 1)

    def test_get_skills_for_ad(self):
        with patch('data.models.Match') as mock_match, \
                patch('data.models.CompanyAd') as mock_company_ad, \
                patch('data.models.Skill') as mock_skill:
            mock_session = Mock(spec=Session)
            skill_1 = ('Python', 'Advanced')
            skill_2 = ('HTTP', 'Beginner')
            mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.all.return_value = \
                (skill_1, skill_2)

            result = professional_services.get_skills(mock_session, mock_company_ad)

            self.assertEqual((skill_1, skill_2), result)
            mock_session.query.return_value.join.return_value.join.return_value. \
                filter.return_value.all.assert_called_once()

    def test_add_skills_to_ad(self):
        with patch('data.models.Skill') as mock_skill:
            mock_session = Mock(spec=Session)
            skills = ['Python - Intermediate', 'SQL - Advanced']

            professional_services.add_skills_to_ad(1, skills, mock_session)

            mock_session.query.assert_called_with(m.Skill.SkillID)
            mock_session.query.return_value.filter.assert_called_with(m.Skill.Description == 'Python')
            mock_session.query.return_value.filter.assert_called_with(m.Skill.Description == 'SQL')
            mock_session.query.return_value.filter.return_value.delete.assert_called_once_with()

    def test_add_skills_to_db(self):
        with patch('data.models.Skill') as mock_skill:
            mock_session = Mock(spec=Session)
            skills = ['Python - Intermediate', 'SQL - Advanced']

            professional_services.add_skills_to_db(skills, mock_session)

            expected_calls = [
                call(mock_skill(Description='Python')),
                call(mock_skill(Description='SQL'))
            ]
            mock_session.add.assert_has_calls(expected_calls, any_order=True)

    def test_add_skills_to_db_withIntegrityError(self):
        with patch('data.models.Skill') as mock_skill:
            mock_session = Mock(spec=Session)
            skills = ['Python - Intermediate']

            mock_session.add.side_effect = sqlalchemy.exc.IntegrityError('Integrity error', None, None)

            professional_services.add_skills_to_db(skills, mock_session)
            mock_session.add.assert_called_once_with(mock_skill(Description='Python'))
            mock_session.rollback.assert_called_once()

    def test_get_all_ads_DescendingOrder(self):
        with patch('data.models.CompanyAd') as mock_company_ad, \
                patch('data.models.CompanyAdSkill') as mock_company_ad_skill, \
                patch('data.models.Skill') as mock_skill:
            mock_session = Mock(spec=Session)
            mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.all.return_value = \
                [('Python', 'Advanced')]
            mock_company_ad_1 = dt.fake_company_ad(CreatedAt=datetime(2023, 12, 3, 11, 15, 00),
                                                   UpdatedAt=datetime(2023, 12, 4, 15, 00, 00))
            mock_company_ad_2 = dt.fake_company_ad(
                CompanyAdID=2,
                BottomSalary='1700',
                TopSalary='2100',
                MotivationDescription='Youtuber wannabe',
                Location='remote',
                CreatedAt=datetime(2023, 12, 3, 11, 15, 00),
                UpdatedAt=datetime(2023, 12, 4, 15, 00, 00)
            )

        mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.order_by.return_value = \
            [mock_company_ad_2, mock_company_ad_1]

        expected = [
            s.CompanyAdsResponse(
                BottomSalary=mock_company_ad_2.BottomSalary,
                TopSalary=mock_company_ad_2.TopSalary,
                MotivationDescription=mock_company_ad_2.MotivationDescription,
                Location=mock_company_ad_2.Location,
                Skills=['Python - Advanced'],
                Status=mock_company_ad_2.Status,
                CompanyAdRequirement=mock_company_ad_2.CompanyAdRequirement,
                CreatedAt=mock_company_ad_2.CreatedAt,
                UpdatedAt=mock_company_ad_2.UpdatedAt
            ),
            s.CompanyAdsResponse(
                BottomSalary=mock_company_ad_1.BottomSalary,
                TopSalary=mock_company_ad_1.TopSalary,
                MotivationDescription=mock_company_ad_1.MotivationDescription,
                Location=mock_company_ad_1.Location,
                Skills=['Python - Advanced'],
                Status=mock_company_ad_1.Status,
                CompanyAdRequirement=mock_company_ad_1.CompanyAdRequirement,
                CreatedAt=mock_company_ad_1.CreatedAt,
                UpdatedAt=mock_company_ad_1.UpdatedAt
            ),
        ]

        result = professional_services.get_all_ads(1, 'desc', mock_session)
        self.assertEqual(expected, result)

    def test_get_all_ads_AscendingOrder(self):
        with patch('data.models.CompanyAd') as mock_company_ad, \
                patch('data.models.CompanyAdSkill') as mock_company_ad_skill, \
                patch('data.models.Skill') as mock_skill:
            mock_session = Mock(spec=Session)
            mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.all.return_value = \
                [('Python', 'Advanced')]
            mock_company_ad_1 = dt.fake_company_ad(CreatedAt=datetime(2023, 12, 3, 11, 15, 00),
                                                   UpdatedAt=datetime(2023, 12, 4, 15, 00, 00))
            mock_company_ad_2 = dt.fake_company_ad(
                CompanyAdID=2,
                BottomSalary='1700',
                TopSalary='2100',
                MotivationDescription='Youtuber wannabe',
                Location='remote',
                CreatedAt=datetime(2023, 12, 3, 11, 15, 00),
                UpdatedAt=datetime(2023, 12, 4, 15, 00, 00)
            )

            mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.order_by.return_value = \
                [mock_company_ad_1, mock_company_ad_2]

            expected = [
                s.CompanyAdsResponse(
                    BottomSalary=mock_company_ad_1.BottomSalary,
                    TopSalary=mock_company_ad_1.TopSalary,
                    MotivationDescription=mock_company_ad_1.MotivationDescription,
                    Location=mock_company_ad_1.Location,
                    Skills=['Python - Advanced'],
                    Status=mock_company_ad_1.Status,
                    CompanyAdRequirement=mock_company_ad_1.CompanyAdRequirement,
                    CreatedAt=mock_company_ad_1.CreatedAt,
                    UpdatedAt=mock_company_ad_1.UpdatedAt
                ),
                s.CompanyAdsResponse(
                    BottomSalary=mock_company_ad_2.BottomSalary,
                    TopSalary=mock_company_ad_2.TopSalary,
                    MotivationDescription=mock_company_ad_2.MotivationDescription,
                    Location=mock_company_ad_2.Location,
                    Skills=['Python - Advanced'],
                    Status=mock_company_ad_2.Status,
                    CompanyAdRequirement=mock_company_ad_2.CompanyAdRequirement,
                    CreatedAt=mock_company_ad_2.CreatedAt,
                    UpdatedAt=mock_company_ad_2.UpdatedAt
                )
            ]

            result = professional_services.get_all_ads(1, 'asc', mock_session)
            self.assertEqual(expected, result)

    def test_get_all_ads_returnEmptyList_whenNoAdsFound(self):
        with patch('data.models.CompanyAd') as mock_company_ad, \
                patch('data.models.CompanyAdSkill') as mock_company_ad_skill, \
                patch('data.models.Skill') as mock_skill:
            mock_session = Mock(spec=Session)
            mock_session.query.return_value.join.return_value.join. \
                return_value.filter.return_value.all.return_value = ()

            mock_session.query.return_value.join.return_value.join.return_value.filter. \
                return_value.order_by.return_value = ()

            expected = []

            result = professional_services.get_all_ads(1, 'asc', mock_session)
            self.assertEqual(expected, result)

    def test_get_ad_returnAd_whenFound(self):
        with patch('data.models.CompanyAd') as mock_company_ad:
            mock_session = Mock(spec=Session)
            mock_company_ad = dt.fake_company_ad()
            mock_session.query.return_value.filter.return_value.first.return_value = mock_company_ad
            result = professional_services.get_ad(1, mock_session)

            self.assertEqual(mock_company_ad, result)
            mock_session.query.return_value.filter.assert_called_with(m.CompanyAd.CompanyAdID == 1)

    def test_get_ad_returnNone_whenNotFound(self):
        mock_session = Mock(spec=Session)
        mock_session.query.return_value.filter.return_value.first.return_value = None
        result = professional_services.get_ad(1, mock_session)

        self.assertIsNone(result)

    def test_return_ad_with_MatchRequests(self):
        mock_session = Mock(spec=Session)
        mock_company_ad = dt.fake_company_ad(
            CreatedAt=datetime(2023, 12, 3, 11, 15, 00),
            UpdatedAt=datetime(2023, 12, 4, 15, 00, 00))
        mock_session.query.return_value.join.return_value.join.return_value.filter.return_value.all.return_value = \
            [('Python', 'Advanced')]
        mock_session.query.return_value.filter.return_value.first.return_value = mock_company_ad
        mock_session.query.return_value.join.return_value.filter.return_value.all.return_value = \
            [s.CompanyAdMatchRequest(CompanyName='Company', MatchStatus='Active',
                                     SentAt=datetime(2023, 12, 1, 14, 12, 0))]
        expected = s.CompanyAdResponseMatch(
            FirstName=mock_company_ad.FirstName,
            LastName=mock_company_ad.LastName,
            BottomSalary=mock_company_ad.BottomSalary,
            TopSalary=mock_company_ad.TopSalary,
            MotivationDescription=mock_company_ad.MotivationDescription,
            Location=mock_company_ad.Location,
            Skills=['Python - Advanced'],
            Status=mock_company_ad.Status,
            CreatedAt=mock_company_ad.CreatedAt,
            UpdatedAt=mock_company_ad.UpdatedAt,
            CompanyAdRequirement=mock_company_ad.CompanyAdRequirement,
            MatchRequests=[s.CompanyAdMatchRequest(
                CompanyName='Company',
                MatchStatus='Active',
                SentAt=datetime(2023, 12, 1, 14, 12, 0))])

        result = professional_services.return_ad(mock_company_ad, mock_session)

        self.assertEqual(expected, result)
        self.assertEqual(['Python - Advanced'], result.Skills)
        self.assertEqual(1, len(result.MatchRequests))

    def test_edit_ad(self):
        with patch('services.professional_services.add_skills_to_db') as mock_add_skills_to_db, \
                patch('services.professional_services.add_skills_to_ad') as mock_add_skills_to_ad:
            mock_session = Mock(spec=Session)
            new_ad = s.CompanyAd(
                BottomSalary='1600',
                TopSalary='1900',
                MotivationDescription='Software Developer',
                Location='Sofia',
                Skills='Python - Advanced'
            )
            mock_company_ad = dt.fake_company_ad()
            mock_add_skills_to_db.return_value = None
            mock_add_skills_to_ad.return_value = None
            mock_session.commit.return_value = None
            mock_session.query.return_value.filter.return_value.first.return_value = dt.fake_company_ad(
                BottomSalary='1600',
                TopSalary='1900',
                MotivationDescription='Software Developer',
                Location='Sofia',
                Skills='Python - Advanced'
            )

            expected = s.CompanyAdResponse(
                    FirstName=mock_company_ad.FirstName,
                    LastName=mock_company_ad.LastName,
                    BottomSalary=new_ad.BottomSalary,
                    TopSalary=new_ad.TopSalary,
                    MotivationDescription=new_ad.MotivationDescription,
                    Location=new_ad.Location,
                    Skills=['Python - Advanced'],
                    Status=mock_company_ad.Status,
                    CreatedAt=mock_company_ad.CreatedAt,
                    UpdatedAt=mock_company_ad.UpdatedAt,
                    CompanyAdRequirement=mock_company_ad.CompanyAdRequirement)

            result = professional_services.edit_ad(new_ad, 1, mock_session)

            self.assertEqual(expected, result)

    def test_set_main_ad(self):
        with patch('data.models.Professional') as mock_professional:
            mock_session = Mock(spec=Session)
            mock_session.query.return_value.filter.return_value.update.return_value = None
            mock_session.commit.return_value = None

            professional_services.set_main_ad(1, 1, mock_session)
            mock_session.query.assert_called_with(mock_professional)

    def test_create_ad(self):
        with patch('services.professional_services.add_skills_to_ad') as mock_add_skills_to_ad:
            mock_session = Mock(spec=Session)
            mock_company_ad = dt.fake_company_ad()
            new_ad = m.CompanyAd(
                ProfessionalID=mock_company_ad.ProfessionalID,
                BottomSalary=mock_company_ad.BottomSalary,
                TopSalary=mock_company_ad.TopSalary,
                MotivationDescription=mock_company_ad.MotivationDescription,
                Location=mock_company_ad.Location,
                CompanyAdRequirement=mock_company_ad.CompanyAdRequirement)

            mock_add_skills_to_ad.return_value = None
            mock_session.commit.return_value = None
            mock_session.add.return_value = None
            mock_session.query.return_value.filter.return_value.first.return_value = mock_company_ad

            expected = s.CompanyAdResponse(
                FirstName=mock_company_ad.FirstName,
                LastName=mock_company_ad.LastName,
                BottomSalary=new_ad.BottomSalary,
                TopSalary=new_ad.TopSalary,
                MotivationDescription=new_ad.MotivationDescription,
                Location=new_ad.Location,
                Skills=['Python - Advanced'],
                Status=mock_company_ad.Status,
                CreatedAt=mock_company_ad.CreatedAt,
                UpdatedAt=mock_company_ad.UpdatedAt,
                CompanyAdRequirement=mock_company_ad.CompanyAdRequirement)


            result = professional_services.create_ad(1, ['Python - Advanced'], new_ad, mock_session)

            self.assertEqual(expected, result)

