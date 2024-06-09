from api.model.db import db


class ProjectAudit(db.Model):
    """Model of the logs for changed made to projects."""
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    operation = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)

    def __init__(self, project_name, email, operation, time, description):
        """
        Args:
            project_name (str): the name of the modified project.
            email (str): the email of the user modifying the project.
            operation (str): the modification performed on the project.
            time (str): the date and time of when the modification occurred.
            description (str): a description of the modification performed.
        """
        self.project_name = project_name
        self.email = email
        self.operation = operation
        self.time = time
        self.description = description
