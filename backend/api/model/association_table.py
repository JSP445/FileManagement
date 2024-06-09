from sqlalchemy import ForeignKey
from api.model.db import db


def create_table(name):
    """Model of a map between tags and assets.

    Args:
        name (str): the name of the mapping table.
    """
    return db.Table(name, db.Model.metadata,
                    db.Column("tag_id", db.Integer, ForeignKey(
                        "tag.tag_id"), primary_key=True),
                    db.Column("asset_id", db.Integer, ForeignKey(
                        "asset.asset_id"), primary_key=True)
                    )


def create_project_map(name):
    """Model of a map between projects and assets.

    Args:
        name (str): the name of the mapping table.
    """
    return db.Table(name, db.Model.metadata,
                    db.Column("project_id", db.Integer, ForeignKey(
                        "project.project_id"), primary_key=True),
                    db.Column("asset_id", db.Integer, ForeignKey(
                        "asset.asset_id"), primary_key=True)
                    )


def create_comment_map(name):
    """Model of a map between parent and reply comments.

    Args:
        name (str): the name of the mapping table.
    """
    return db.Table(name, db.Model.metadata,
                    db.Column("parent_id", db.Integer, ForeignKey(
                        "comment.id"), primary_key=True),
                    db.Column("reply_id", db.Integer, ForeignKey(
                        "comment.id"), primary_key=True)
                    )
