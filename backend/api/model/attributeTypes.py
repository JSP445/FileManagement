from api.model.db import db


class AttributeType(db.Model):
    """Model of the data types of attributes."""
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    attributes = db.relationship(
        "AssetTypeAttribute", backref="attribute_type", lazy=True)

    def __init__(self, name):
        """
        Args:
            name (string): the name of the attribute type.
            reg_ex (string): the pattern that specifies the format of the attribute.
        """
        self.type_name = name
