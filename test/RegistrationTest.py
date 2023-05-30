"""
Test file for the registration form.

Compares the retrieved redirected link to the expected result

NOTE:
    - test_valid_registration_form doesn't work due to it not retrieving the redirected link correctly therefore the
      data has been tested manually and returned the expected result.
    - due to the redirected link not being retrieved correctly the results of the other tests aren't reliable therefore
      the data has been tested manually and all returned the expected result.
"""

import unittest
from app import app


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_valid_registration_form(self):
        """Test case for a correct registration from the user."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Test1!',
            'confirm_password': 'Test1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/login', response.request.path)

    def test_invalid_email(self):
        """Test case for an invalid email from the user."""
        response = self.app.post('/register', data={
            'email': 'failedtest',
            'username': 'test',
            'password': 'Test1!',
            'confirm_password': 'Test1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_used_email(self):
        """Test case for an email already used in the database."""
        response = self.app.post('/register', data={
            'email': 'admin@email.com',
            'username': 'test',
            'password': 'Test1!',
            'confirm_password': 'Test1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_invalid_username(self):
        """Test case for an invalid username from the user."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'failed!test',
            'password': 'Test1!',
            'confirm_password': 'Test1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_missing_uppercase_password(self):
        """Test case for an invalid password not including an uppercase character."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'failtest1!',
            'confirm_password': 'failtest1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_missing_lowercase_password(self):
        """Test case for an invalid password not including a lowercase character."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'FAILTEST1!',
            'confirm_password': 'FAILTEST1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_missing_number_password(self):
        """Test case for an invalid password not including a numerical character."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Failtest!',
            'confirm_password': 'Failtest!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_missing_special_password(self):
        """Test case for an invalid password not including a special character."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Failtest1',
            'confirm_password': 'Failtest1'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_not_equal_password(self):
        """Test case for a confirm_password and password not matching."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Failtest1!',
            'confirm_password': 'Test1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)

    def test_invalid_length_password(self):
        """Test case for an invalid password of an incorrect length."""
        response = self.app.post('/register', data={
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Failingtest1!',
            'confirm_password': 'Failingtest1!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual('/register', response.request.path)


if __name__ == '__main__':
    unittest.main()
