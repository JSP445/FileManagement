from api.model.db import db


class Role(db.Model):
    """Model of the different roles that users can have in the application."""
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    security_level = db.Column(db.Integer, unique=True, nullable=False)
    users = db.relationship("User", backref="role", lazy=True)

    def __init__(self, name, security_level):
        """
        Args:
            name (str): the name of the role.
            security_level (int): a numeric that represents what the role can access.
        """
        self.name = name
        self.security_level = security_level
