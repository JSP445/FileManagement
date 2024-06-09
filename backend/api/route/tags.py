from flask import Blueprint, jsonify
from api.model.tags import Tag
from api.schema.tags import tag_name_schema
from api.route.roles import security_level_required

tag_api = Blueprint("tag", __name__)


@tag_api.route("/", methods=["GET"])
@security_level_required(25)
def getTags():
    """Gets all the tags in the database.

    Returns:
        all_tags (json): A list of all tags in database as tag objects.
    """
    return jsonify(tag_name_schema.dump(Tag.query.all())), 200
