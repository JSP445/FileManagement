from flask import Blueprint, jsonify, request
from api.route.roles import security_level_required
from api.model.comment import Comment, association_table
from api.schema.comments import comment_schema, single_comment_schema
from api.utils.validation import required_parameters
from api.model.db import db

comment_api = Blueprint("comment", __name__)


@comment_api.route("/", methods=["GET"])
@security_level_required(25)
def getAllComments():
    """Gets all comments for all assets.

    Returns:
        all_comments (json): List of all comments in database as comment objects.
    """
    return jsonify(comment_schema.dump(Comment.query.all())), 200


@comment_api.route("/<int:asset_id>", methods=["GET"])
@security_level_required(25)
def getComments(asset_id):
    """Gets all comments for a single asset.

    Args:
        asset_id (int): the id of the asset.

    Returns:
        requested_comment (json): Requested comment as comment objects.
    """
    return jsonify(comment_schema.dump(Comment.query.filter_by(asset_id=asset_id).all())), 200


@comment_api.route("/", methods=["POST"])
@required_parameters(["asset_id", "message"])
@security_level_required(50)
def addComment(current_user):
    """Adds comment for asset. Also used for reply comments.

    Returns:
        response (json): Success message.
    """
    data = request.get_json()
    parent = None

    # Checks if comment is a reply
    if "reply_id" in data and data["reply_id"] != None:
        parent = Comment.query.filter_by(id=data["reply_id"]).first()

        if parent == None:
            return jsonify({"message": "Parent comment not found."}), 404

        if parent.asset_id != data["asset_id"]:
            return jsonify({"message": "Incorrect parameters: Reply must be on same asset as parent."}), 400

    comment = Comment(data["message"], data["asset_id"], current_user["id"])

    if parent:
        comment.reply_to = parent

    db.session.add(comment)

    db.session.commit()

    return jsonify({"message": "Comment successful created."}), 201


@comment_api.route("/<int:comment_id>", methods=["DELETE"])
@security_level_required(50)
def deleteComment(comment_id, current_user):
    """"Deletes a single comment and all replies to it.

    Args:
        comment_id (int): the id of the comment to be deleted.

    Returns:
        deleted_comment (json): Deleted comment as a comment object.
    """
    comment = Comment.query.filter_by(id=comment_id).first()

    if comment == None:
        return jsonify({"message": "Comment not found"}), 404

    if comment.user_id != current_user["id"]:
        return jsonify({"message": "Cannot delete another user's comment"}), 403

    # Gets all replies to the comment
    replies = db.session.query(association_table).filter(
        association_table.c.parent_id == comment_id).all()

    # Deletes all replies
    for reply in replies:
        Comment.query.filter_by(id=reply.reply_id).delete()

    res = single_comment_schema.dump(comment)
    db.session.delete(comment)
    db.session.commit()

    return jsonify(res), 200
