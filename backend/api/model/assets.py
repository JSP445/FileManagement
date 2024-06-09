from api.model.db import db


class Asset(db.Model):
    """Model of an asset that will be stored in the database."""
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(50), unique=True, nullable=False)
    asset_type_id = db.Column(db.Integer, db.ForeignKey(
        "asset_type.asset_type_id"), nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_on = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    attribute_values = db.relationship(
        "AssetAttribute", backref="asset", lazy=True, cascade="all, delete")

    def __init__(self, name, typeid, createdBy, createdOn):
        """
        Args:
            name (str): the name of the asset.
            typeid (int): the id of the corresponding asset type.
            createdBy (int): the id of the user who created the asset.
            createdOn (str): the time that the asset was created.
        """
        self.asset_name = name
        self.asset_type_id = typeid
        self.created_by_user_id = createdBy
        self.created_on = createdOn
        self.last_updated = createdOn


class AssetAttribute(db.Model):
    """Model of the attributes of an asset."""
    asset_attribute_id = db.Column(db.Integer, primary_key=True)
    attribute_value = db.Column(db.String(50), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey(
        "asset.asset_id"), nullable=False)
    asset_attribute_type_id = db.Column(db.Integer, db.ForeignKey(
        "asset_type_attribute.asset_attribute_id"), nullable=False)

    def __init__(self, value, asset_id, asset_attribute_type_id):
        """
        Args:
            value (str): the value of the attribute.
            asset_id (int): the id of the corresponding asset.
            asset_attribute_type_id (int): the id of the corresponding type of asset attribute.
        """
        self.attribute_value = value
        self.asset_id = asset_id
        self.asset_attribute_type_id = asset_attribute_type_id
