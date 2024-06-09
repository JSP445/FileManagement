from api.model.role import Role
from api.model.attributeTypes import AttributeType
from api.model.assetTypes import AssetType, AssetTypeAttribute
from api.model.db import db

DEFAULT_ROLES = [
    {
        "name": "Admin",
        "level": 100
    },
    {
        "name": "Normal",
        "level": 50
    },
    {
        "name": "Viewer",
        "level": 25
    }
]

DEFAULT_ATTRIBUTE_TYPES = [
    {
        "name": "String"
    },
    {
        "name": "Integer"
    }
]

DEFAULT_ASSET_TYPE = [
    {
        "asset_type_id": 0,
        "asset_type_name": "Default Asset Type",
        "attributes": [
            {"asset_type_id": 0, "attribute_name": "Description",
                "attribute_type_id": 1},
            {"asset_type_id": 0, "attribute_name": "Location", "attribute_type_id": 1},
        ]
    }
]


def setup_database():
    """Initiates all tables in the database."""
    db.create_all()


def setup_attribute_types():
    """Sets the data types of the asset type attributes into the database."""
    for attr_type in DEFAULT_ATTRIBUTE_TYPES:
        if not AttributeType.query.filter_by(type_name=attr_type["name"]).first():
            attr_type = AttributeType(attr_type["name"])
            db.session.add(attr_type)

    db.session.commit()


def setup_default_asset_type():
    """Sets all the default asset types into the database."""
    for asset_type in DEFAULT_ASSET_TYPE:
        for attribute in asset_type["attributes"]:
            if not AssetTypeAttribute.query.filter_by(asset_type_id=attribute["asset_type_id"], attribute_name=attribute["attribute_name"]).first():
                attribute = AssetTypeAttribute(
                    attribute["asset_type_id"], attribute["attribute_name"], attribute["attribute_type_id"])
                db.session.add(attribute)

        if not AssetType.query.filter_by(asset_type_id=asset_type["asset_type_id"]).first():
            asset_type = AssetType(asset_type["asset_type_name"], 1)
            asset_type.set_id(0)
            db.session.add(asset_type)

    db.session.commit()


def setup_roles():
    """Sets all the default roles into the database."""
    for role in DEFAULT_ROLES:
        if not Role.query.filter_by(name=role["name"]).first():
            role = Role(role["name"], role["level"])
            db.session.add(role)

    db.session.commit()
