from api.model.association_table import create_comment_map
from sqlalchemy.orm import backref
from api.model.db import db

association_table = create_comment_map("comment_map")


class Comment(db.Model):
    """Model of the comments that are applied to assets."""
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey(
        "asset.asset_id"), nullable=False)
    asset = db.relationship("Asset", backref=backref(
        "comments", cascade="all, delete"))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_by = db.relationship("User", backref=backref(
        "comments", cascade="all, delete"), uselist=False, lazy=True)
    replies = db.relationship("Comment", secondary=association_table, primaryjoin=association_table.c.parent_id == id, secondaryjoin=association_table.c.reply_id == id, backref=backref(
        "reply_to", uselist=False))

    def __init__(self, message, asset_id, user_id):
        """
        Args:
            message (str): the comment applied to an asset.
            asset_id (int): the id of the asset that is commented to.
            user_id (int): the id of the user presenting the comments.
        """
        self.message = message
        self.asset_id = asset_id
        self.user_id = user_id
