from flask import Flask
from unittest import TestCase
from app import create_app
from api.model.db import db
from json import dumps
import jobs


class TestAssets(TestCase):

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

    def test_no_name(self):
        """Tests if no asset name is provided."""
        json = {
            "asset_type_id": 1
        }
        errormessage = {"message": "Missing required parameter: asset_name."}

        res = self.app.post(
            "asset/add", headers=self.headers, data=dumps(json))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_no_asset_type_id(self):
        """Tests if no asset type is provided."""
        json = {
            "asset_name": "my new kinda asset"
        }
        errormessage = {
            "message": "Missing required parameter: asset_type_id."}

        res = self.app.post(
            "asset/add", headers=self.headers, data=dumps(json))

        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)
