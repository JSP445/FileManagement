from api.model.db import db
from api.model.association_table import create_project_map

project_map = create_project_map("project_map")


class Project(db.Model):
    """Model of a project that utilises the assets."""
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), unique=True, nullable=False)
    project_description = db.Column(db.String(4096), nullable=False)
    assets = db.relationship("Asset", secondary=project_map, backref=db.backref(
        "projects", uselist=True), lazy=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, name, desc, user_id):
        """
        Args:
            name (str): the name of the project.
            desc (str): a description of the project given by the creator.
            user_id (int): the id of the user who created the project.
        """
        self.project_name = name
        self.project_description = desc
        self.created_by_id = user_id
