from api.model.db import db


class UserName(db.Model):
    """Model of the details for users in the database."""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False, default="first_name")
    last_name = db.Column(db.String(40), nullable=False, default="last_name")
    nickname = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref("user_name", uselist=False, cascade="all, delete"), lazy=True)

    def __init__(self, first_name, last_name, user_id):
        """
        Args:
            first_name (str): the first name of the user.
            last_name (str): the last name of the user.
            user_id (id): the id of the user.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
