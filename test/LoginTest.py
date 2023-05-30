"""
Test file for the login form.

Compares the retrieved redirected link to the expected result

NOTE:
    - test_valid_login_form doesn't work due to it not retrieving the redirected link correctly therefore the
      data has been tested manually and returned the expected result.
    - due to the redirected link not being retrieved correctly the results of the other tests aren't reliable therefore
      the data has been tested manually and all returned the expected result.
"""

import unittest
import pyotp
from app import app


class LoginTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_valid_login_form(self):
        """Test case for a correct login from the user."""
        totp = pyotp.TOTP('CXIVWGAW3ISLJ77LZM26JFGW5CUCQVIO')
        pinkey = totp.now()

        response = self.app.post('/login', data={
            'email': 'admin@email.com',
            'password': 'Admin1!',
            'pin': pinkey,
            'recaptcha': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, '/admin')

    def test_incorrect_email(self):
        """Test case for an incorrect email from the user."""
        totp = pyotp.TOTP('CXIVWGAW3ISLJ77LZM26JFGW5CUCQVIO')
        pinkey = totp.now()

        response = self.app.post('/login', data={
            'email': 'failed@test.com',
            'password': 'Admin1!',
            'pin': pinkey,
            'recaptcha': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, '/login')

    def test_incorrect_password(self):
        """Test case for an incorrect password from the user."""
        totp = pyotp.TOTP('CXIVWGAW3ISLJ77LZM26JFGW5CUCQVIO')
        pinkey = totp.now()

        response = self.app.post('/login', data={
            'email': 'admin@email.com',
            'password': 'Fail1!',
            'pin': pinkey,
            'recaptcha': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, '/login')

    def test_incorrect_pin(self):
        """Test case for an incorrect pin from the user."""
        response = self.app.post('/login', data={
            'email': 'admin@email.com',
            'password': 'Admin1!',
            'pin': '12345',
            'recaptcha': True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, '/login')

    def test_incorrect_recaptcha(self):
        """Test case for an incorrect recaptcha from the user."""
        totp = pyotp.TOTP('CXIVWGAW3ISLJ77LZM26JFGW5CUCQVIO')
        pinkey = totp.now()

        response = self.app.post('/login', data={
            'email': 'admin@email.com',
            'password': 'Admin1!',
            'pin': pinkey,
            'recaptcha': False
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, '/login')


if __name__ == '__main__':
    unittest.main()
