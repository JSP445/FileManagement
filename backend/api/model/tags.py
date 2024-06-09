from api.model.db import db
from api.model.association_table import create_table

association_table = create_table("tag_map")


class Tag(db.Model):
    """Model for the tags that can be used to give extra details to assets."""
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), unique=True, nullable=False)
    assets = db.relationship(
        "Asset", secondary=association_table, backref="tags")

    def __init__(self, tag_name):
        """
        Args:
            tag_name (str): the name of the tag.
        """
        self.tag_name = tag_name
