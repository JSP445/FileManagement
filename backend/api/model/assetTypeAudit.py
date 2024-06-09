from api.model.db import db


class AssetTypeAudit(db.Model):
    """Model of the logs for changes made to asset types."""
    id = db.Column(db.Integer, primary_key=True)
    asset_type_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    operation = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)

    def __init__(self, asset_type_name, email, operation, time, description):
        """
        Args:
            asset_type_name (str): the name of the modified asset type.
            email (str): the email of the user modifying the asset type.
            operation (str): the modification performed on the asset type.
            time (str): the date and time of when the modification occurred.
            description (str): a description of the modification performed.
        """
        self.asset_type_name = asset_type_name
        self.email = email
        self.operation = operation
        self.time = time
        self.description = description
