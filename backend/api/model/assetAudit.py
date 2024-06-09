from api.model.db import db


class AssetAudit(db.Model):
    """Model of the logs for changes made to assets."""
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    operation = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)

    def __init__(self, asset_name, email, operation, time, description):
        """
        Args:
            asset_name (str): the name of the modified asset.
            email (str): the email of the user modifying the asset.
            operation (str): the modification performed on the asset.
            time (str): the date and time of when the modification occurred.
            description (str): a description of the modification performed.
        """
        self.asset_name = asset_name
        self.email = email
        self.operation = operation
        self.time = time
        self.description = description
