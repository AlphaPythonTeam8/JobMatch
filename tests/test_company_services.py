import unittest
from unittest.mock import patch, MagicMock
from data import schemas
from services import company_services
from sqlalchemy.orm import Session
import data.models as m

class TestCompanyServices(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.company_data = schemas.CompanyRegistration(
            Username="CompanyX",
            CompanyName="CompanyX",
            Email="contact@companyx.com",
            Password="StrongPassword123!",
            VerificationToken="some_verification_token"
        )

        self.company = m.Company(
            CompanyID=1,
            Username="CompanyX",
            CompanyName="CompanyX",
            Email="contact@companyx.com",
            Password="StrongPassword123!",
            VerificationToken="verification_token",
            EmailVerified=False
        )

    def test_register_company(self):
        with patch('services.company_services.hash_password') as mock_hash_password, \
             patch('services.company_services.generate_verification_token') as mock_verification_token, \
             patch('services.company_services.send_verification_email') as mock_send_email:

            mock_hash_password.return_value = "hashedpassword"
            mock_verification_token.return_value = "verification_token"
            self.db.add.return_value = None
            self.db.commit.return_value = None
            self.db.refresh.return_value = None

            result = company_services.register(self.company_data, self.db)
            if isinstance(result, dict):
                self.assertEqual(result["message"], f"Email address {self.company_data.Email} is already in use.")
            else:
                self.assertEqual(result.CompanyName, self.company_data.CompanyName)
                self.assertEqual(result.Username, self.company_data.Username)
                self.assertEqual(result.Email, self.company_data.Email)
                self.assertEqual(result.VerificationToken, "verification_token")
                mock_hash_password.assert_called_once_with(self.company_data.Password)
                mock_verification_token.assert_called_once()
                mock_send_email.assert_called_once_with(self.company_data.Email, "verification_token")


    def test_update_company_info(self):
        new_info = schemas.CompanyUpdate(
            Description="Updated Description",
            Location="Updated Location",
            Contact="Updated Contact"
        )
        # Mock the behavior of the session after update
        self.db.query.return_value.filter.return_value.first.return_value = self.company
        self.company.Description = "Updated Description"  # Simulate the update

        result = company_services.update_info(1, new_info, self.db)

        self.assertEqual(result.Description, new_info.Description)


    def test_view_company_info(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.company

        result = company_services.view_company_info(1, self.db)

        self.assertEqual(result.Username, self.company.Username)
        self.assertEqual(result.CompanyName, self.company.CompanyName)
        self.assertEqual(result.Email, self.company.Email)

    def test_get_match_requests_for_ad(self):
        match_requests = [("Pending", "2023-01-01", "John")]
        self.db.query.return_value.join.return_value.filter.return_value.all.return_value = match_requests

        result = company_services.get_match_requests_for_ad(1, self.db)

        self.assertEqual(result, match_requests)

    def test_change_password(self):
        new_password = "NewPassword123!"
        confirm_new_password = "NewPassword123!"
        self.db.query.return_value.filter.return_value.first.return_value = self.company

        result = company_services.change_password(1, new_password, confirm_new_password, self.db)

        self.db.commit.assert_called_once()
        self.assertEqual(result["message"], "Password changed successfully")

if __name__ == '__main__':
    unittest.main()
