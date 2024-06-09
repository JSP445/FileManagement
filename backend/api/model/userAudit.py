from api.model.db import db


class UserAudit(db.Model):
    """Model of the logs made for changes made to users."""
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(40), nullable=False)
    subject_role = db.Column(db.String(25))
    admin = db.Column(db.String(40), nullable=False)
    operation = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self, subject, subject_role, admin, operation, time):
        """
        Args:
            subject (str): the email of the user being modified.
            subject_role (str): the role of the user being modified.
            admin (str): the email of the admin user modifying the user.
            operation (str): the modification performed on the user. 
            time (str): the date and time of when the modification occurred.
        """
        self.subject = subject
        self.subject_role = subject_role
        self.admin = admin
        self.operation = operation
        self.time = time
