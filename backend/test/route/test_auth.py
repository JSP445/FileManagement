from unittest import TestCase
from app import create_app
from api.model.db import db
from api.model.user import User
from json import dumps
import jobs
import jwt


class TestAuth(TestCase):

    @classmethod
    def setUpClass(self):
        """Sets initial data for testing."""
        self.base = create_app(True)
        self.app = self.base.test_client()

        self.headers = {"content-type": "application/json"}
        self.json = {
            "email": "admin@example.com",
            "password": "P@ssw0rd"
        }

    def setUp(self):
        """Sets up each test by authenticating."""
        with self.base.app_context():
            db.drop_all()
            db.create_all()
            jobs.run()
            res = self.app.post(
                "auth/login", data=dumps(self.json), headers=self.headers)
            self.token = "Bearer " + res.get_json()["token"]
            self.headers["Authorization"] = self.token

    def tearDown(self):
        """Resets the database for each test."""
        with self.base.app_context():
            db.drop_all()

    def test_invalid_content_type(self):
        """Tests that an error is thrown if the wrong content type is used."""

        headers = {"content-type": "application/xml",
                   "Authorization": self.token}

        error_message = {"message": "Invalid content type."}
        res = self.app.post("auth/register", headers=headers)

        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 415)

    def test_missing_email(self):
        """Tests that an error is thrown if an email address is not provided when registering."""

        json = {"password": "password"}
        error_message = {"message": "Missing required parameter: email."}

        res = self.app.post(
            "auth/register", headers=self.headers, data=dumps(json))

        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_missing_password(self):
        """Tests that an error is thrown if a password is not provided when registering."""

        json = {"email": "someone@example.com"}
        error_message = {"message": "Missing required parameter: password."}

        res = self.app.post(
            "auth/register", headers=self.headers, data=dumps(json))

        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_invalid_emails(self):
        """Tests that an error is thrown if an invalid email address is entered when registering."""

        error_message = {"message": "Invalid email address."}

        json1 = {"email": "@example.com", "password": "password"}
        json2 = {"email": "someone@", "password": "password"}
        json3 = {"email": "example.com", "password": "password"}

        res = self.app.post(
            "auth/register", headers=self.headers, data=dumps(json1))
        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 400)

        res = self.app.post(
            "auth/register", headers=self.headers, data=dumps(json2))
        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 400)

        res = self.app.post(
            "auth/register", headers=self.headers, data=dumps(json3))
        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_duplicate_users(self):
        """Tests that an error will be thrown if a new account tries to use the email address of an account that already exists."""

        error_message = {
            "message": "Account with email address already exists."}

        res = self.app.post(
            "auth/register", headers=self.headers, data=dumps(self.json))
        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_incorrect_creds(self):
        """Tests that an error will be thrown if the incorrect email address or password is entered."""

        error_message = {"message": "Incorrect email address or password."}

        added_json = {
            "email": "manav@example.com",
            "password": "P@ssw0rd!",
            "role_id": 1
        }

        unregistered_json1 = {
            "email": "manav@example.com",
            "password": "123456",
            "role_id": 1
        }

        unregistered_json2 = {
            "email": "no@example.com",
            "password": "P@ssw0rd!",
            "role_id": 1
        }

        success_message = {
            "message": "User created.",
            "user": {
                "email": added_json["email"]
            }
        }

        res = self.app.post(
            "auth/register", headers=self.headers, data=dumps(added_json))
        self.assertEqual(success_message, res.get_json())
        self.assertEqual(res.status_code, 201)

        res = self.app.post("auth/login", headers=self.headers,
                            data=dumps(unregistered_json1))
        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 401)

        res = self.app.post("auth/login", headers=self.headers,
                            data=dumps(unregistered_json2))
        self.assertEqual(error_message, res.get_json())
        self.assertEqual(res.status_code, 401)

    def test_successful_login(self):
        """Tests that a token will be provided if the user logs in successfully."""

        res = self.app.post(
            "auth/login", headers=self.headers, data=dumps(self.json))
        jwt.decode(res.get_json()[
                   "token"], self.base.config["SECRET_KEY"], algorithms=["HS256"])

        login_success = {
            "message": "Login Successful.",
            "token": res.get_json()["token"]
        }

        self.assertEqual(login_success["message"], res.get_json()["message"])
        self.assertEqual(res.status_code, 200)
