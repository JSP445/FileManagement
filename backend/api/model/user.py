from werkzeug.security import generate_password_hash
from api.model.db import db


class User(db.Model):
    """Model of a user that will be stored in the database."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    asset_types = db.relationship("AssetType", backref="created_by", lazy=True)
    assets = db.relationship("Asset", backref="created_by", lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"))
    projects = db.relationship("Project", backref="created_by", lazy=True)
    deprecated = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, role_id):
        """
        Args:
            email (str): the email address of the user.
            password (str): the password for the user's account.
            role_id (int): the user's role, which determines what the user can access.
        """

        self.email = email
        self.password = generate_password_hash(password, method="sha256")
        self.role_id = role_id

    def to_dict(self):
        """Returns the attributes as a dictionary."""
        return dict(id=self.id, email=self.email, password=self.password)
