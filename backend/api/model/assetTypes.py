from api.model.db import db


class AssetType(db.Model):
    """Model of the types that distinguish assets."""
    asset_type_id = db.Column(db.Integer, primary_key=True)
    asset_type_name = db.Column(db.String(50), unique=True, nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    inherited_from = db.Column(db.Integer, db.ForeignKey(
        'asset_type.asset_type_id'), default=0)
    attributes = db.relationship(
        'AssetTypeAttribute', backref='asset_type', lazy=True, cascade="all, delete")
    assets = db.relationship(
        'Asset', backref='asset_type', lazy=True, cascade="all, delete")
    children = db.relationship('AssetType', backref=db.backref(
        'parent', uselist=False, remote_side=[asset_type_id]), lazy=True)

    def __init__(self, name, createdBy):
        """
        Args:
            name (str): the name of the asset type.
            createdBy (int): the id of the user who created the asset type.
        """
        self.asset_type_name = name
        self.created_by_user_id = createdBy

    def set_id(self, id):
        """Explicitly sets the id of an asset type."""
        self.asset_type_id = id

    def set_parent(self, id):
        """Sets a parent asset type to inherit attributes from."""
        self.inherited_from = id


class AssetTypeAttribute(db.Model):
    """Model of the attributes of an asset type."""
    asset_attribute_id = db.Column(db.Integer, primary_key=True)
    asset_type_id = db.Column(db.Integer, db.ForeignKey(
        "asset_type.asset_type_id"), nullable=False)
    attribute_name = db.Column(db.String, nullable=False)
    attribute_type_id = db.Column(db.Integer, db.ForeignKey(
        "attribute_type.type_id"), nullable=False, default=1)
    attribute_values = db.relationship(
        'AssetAttribute', backref=db.backref('attribute_name', uselist=False), lazy=True)

    def __init__(self, *args):
        self.asset_type_id = args[0]
        self.attribute_name = args[1]
        if len(args) > 2:
            self.attribute_type_id = args[2]
