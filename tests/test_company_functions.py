import unittest

from sqlalchemy.orm import Session

from services.company_services import register
import unittest
from unittest.mock import patch, MagicMock, Mock

from data_test import fake_company


class TestRegisterFunction(unittest.TestCase):

    def test_register_success(self):

        # Setup mock objects and return values

        db = Mock(spec=Session)
        mock_company_registration = fake_company()

        # Call the register function
        with patch('common.hashing.hash_password', return_value='hashed_password') as mock_hash_password, \
                patch('common.oauth2.generate_verification_token',
                      return_value='verification_token') as mock_generate_token, \
                patch('data.models.Company') as mock_company_class:
            mock_company_instance = MagicMock()
            mock_company_class.return_value = mock_company_instance
            mock_company_instance.Password = 'hashed_password'
            mock_company_instance.VerificationToken = 'verification_token'

            result = register(mock_company_registration, db)

            # Assertions
            self.assertEqual(result.Password, 'hashed_password')
            self.assertEqual(result.VerificationToken, 'verification_token')
            self.assertIs(result, mock_company_instance, "The returned object is not the mock instance")

            db.add.assert_called_with(result)
            db.commit.assert_called()
            db.refresh.assert_called_with(result)

            # Assertion: if hash password was called with hash_password(user.Password)

            mock_hash_password.assert_called_with(mock_company_registration.Password)
