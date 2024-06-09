from json import dumps
from unittest import TestCase
from app import create_app
from api.model.db import db
import jobs


class TestAssetTypes(TestCase):

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

    def test_not_json_add(self):
        """Tests incorrect content type."""
        self.headers = {
            "content-type": ""
        }
        errormessage = {"message": "Invalid content type."}

        res = self.app.post("asset/type/", headers=self.headers)
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 415)

    def test_no_asset_type_name_add(self):
        """Tests if asset type name is not provided."""
        json = {
            "created_by": 1,
        }
        errormessage = {
            "message": "Missing required parameter: asset_type_name."}

        res = self.app.post(
            "asset/type/", headers=self.headers, data=dumps(json))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_non_unique_asset_name_edit_type(self):
        """Tests if asset name is not unique for another name."""
        json = {
            "asset_type_name": "Test Asset 1",
            "parent_asset_type": 0,
        }

        self.app.post("asset/type/", headers=self.headers, data=dumps(json))

        errormessage = {
            "message": "Asset type name already in database. Choose a different name."}
        res = self.app.post(
            "asset/type/", headers=self.headers, data=dumps(json))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_no_asset_type_id_update(self):
        """Tests if no asset type id is provided."""
        json = {
            "asset_type_name": "new name",
            "attributes": []
        }

        errormessage = {
            "message": "Missing required parameter: asset_type_id."}
        res = self.app.patch("asset/type/",
                             headers=self.headers, data=dumps(json))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_no_asset_type_name_update(self):
        """Tests if no asset type name is provided."""
        json = {
            "asset_type_id": 1,
            "attributes": []
        }

        errormessage = {
            "message": "Missing required parameter: asset_type_name."}
        res = self.app.patch("asset/type/",
                             headers=self.headers, data=dumps(json))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_no_attributes_update(self):
        """Tests if no attributes are provided."""
        json = {
            "asset_type_id": 1,
            "asset_type_name": "new name"
        }

        errormessage = {"message": "Missing required parameter: attributes."}
        res = self.app.patch("asset/type/",
                             headers=self.headers, data=dumps(json))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_no_asset_type_found_update(self):
        """Tests if asset type is not in database."""
        json = {
            "parent_asset_type": 1,
            "asset_type_id": 10768,
            "asset_type_name": "new name",
            "attributes": []
        }

        errormessage = {
            "message": "Asset type selected not found in database."}
        res = self.app.patch("asset/type/",
                             headers=self.headers, data=dumps(json))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 404)

    def test_no_attribute_name_update(self):
        """Tests if attribute name is not provided."""
        jsonCreate = {
            "parent_asset_type": 1,
            "asset_type_name": "new name",
            "attributes": [{"name": "Test Attribute 1"}]
        }

        resCreate = self.app.post(
            "asset/type/", headers=self.headers, data=dumps(jsonCreate))
        self.assertEqual(resCreate.status_code, 201)

        id = resCreate.get_json()["asset_type_id"]

        jsonError = {
            "asset_type_id": id,
            "asset_type_name": "new name",
            "attributes": [
                {
                    "asset_attribute_id": 1,
                }
            ]
        }

        errormessage = {
            "message": "Missing required parameter: attribute_name."}

        resError = self.app.patch(
            "asset/type/", headers=self.headers, data=dumps(jsonError))
        self.assertEqual(errormessage, resError.get_json())
        self.assertEqual(resError.status_code, 400)

    def test_non_unique_asset_type_name_update(self):
        """Tests editing an asset to the name of another asset."""
        jsonCreate1 = {
            "parent_asset_type": 1,
            "asset_type_name": "Test Type 1",
            "created_by": 1,
        }

        jsonCreate2 = {
            "parent_asset_type": 1,
            "asset_type_name": "Test Type 2",
            "created_by": 1,
        }

        jsonError = {
            "asset_type_id": 1,
            "asset_type_name": "Test Type 2",
            "attributes": [
            ]
        }

        errormessage = {"message": "Another asset type already has this name."}

        self.app.post("asset/type/", headers=self.headers,
                      data=dumps(jsonCreate1))
        self.app.post("asset/type/", headers=self.headers,
                      data=dumps(jsonCreate2))
        res = self.app.patch("asset/type/",
                             headers=self.headers, data=dumps(jsonError))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

    def test_new_non_unique_attribute_name_update(self):
        """Tests if duplicate attribute names are provided."""
        jsonCreate = {
            "parent_asset_type": 1,
            "asset_type_name": "Test Type 1",
            "created_by": 1,
            "attributes": [{"type_id": 1, "name": "Test Attribute 1"}, {"type_id": 1, "name": "Test Attribute 2"}]
        }

        res = self.app.post(
            "asset/type/", headers=self.headers, data=dumps(jsonCreate))
        id = res.get_json()["asset_type_id"]

        jsonError = {
            "asset_type_id": id,
            "asset_type_name": "Test Type 1",
            "attributes": [
                {
                    "attribute_type_id": 1,
                    "asset_attribute_id": -1,
                    "attribute_name": "Test Attribute 1"
                },
                {
                    "attribute_type_id": 1,
                    "asset_attribute_id": 1,
                    "attribute_name": "Test Attribute 1"
                },
                {
                    "attribute_type_id": 1,
                    "asset_attribute_id": 2,
                    "attribute_name": "Test Attribute 2"
                }
            ]
        }

        errormessage = {
            "message": "An attribute of this asset type already has this name."}

        res = self.app.patch("asset/type/",
                             headers=self.headers, data=dumps(jsonError))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)

# Using value >2 due to default values of asset attribute.
    def test_attribute_not_found_update(self):
        """Tests if a provided attribute is not in the database."""
        jsonCreate1 = {
            "parent_asset_type": 1,
            "asset_type_name": "Test Type 1",
            "asset_type_id": 1,
            "attributes": []
        }

        jsonError = {
            "asset_type_id": 1,
            "asset_type_name": "Test Type 1",
            "attributes": [
                {
                    "asset_attribute_id": 3,
                    "attribute_name": "Test Attribute 1",
                    "attribute_type_id": 1,
                }
            ]
        }

        errormessage = {
            "message": "An asset attribute selected was not found in the database."}

        self.app.post("asset/type/", headers=self.headers,
                      data=dumps(jsonCreate1))
        res = self.app.patch(
            "asset/type/", headers=self.headers, data=dumps(jsonError))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 404)

    def test_updated_non_unique_attribute_name_update(self):
        """Tests if duplicate attribute names are provided."""
        jsonCreate1 = {
            "asset_type_name": "Test Type 1",
            "parent_asset_type": 1,
            "attributes": [{"asset_attribute_id": 1, "name": "Test Attribute 1"}, {"asset_attribute_id": 2, "name": "Test Attribute 2"}]
        }

        jsonError = {
            "asset_type_id": 1,
            "asset_type_name": "Test Type 1",
            "attributes": [
                {
                    "asset_attribute_id": 1,
                    "attribute_type_id": 1,
                    "attribute_name": "Test Attribute 1"
                },
                {
                    "asset_attribute_id": 2,
                    "attribute_type_id": 2,
                    "attribute_name": "Test Attribute 1"
                }
            ]
        }

        errormessage = {
            "message": "An attribute of this asset type already has this name."}
        res = self.app.post(
            "asset/type/", headers=self.headers, data=dumps(jsonCreate1))
        res = self.app.patch("asset/type/",
                             headers=self.headers, data=dumps(jsonError))
        self.assertEqual(errormessage, res.get_json())
        self.assertEqual(res.status_code, 400)
