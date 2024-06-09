from api.model.user import User
from api.schema.users import user_schema, single_user_schema
from api.route.roles import security_level_required
from api.utils.validation import required_parameters
from api.model.user_name import UserName
from api.route.auth import check_password_hash
from werkzeug.security import generate_password_hash
from flask import Blueprint, jsonify, request
import api.utils.userAudit as audit
from api import DEFAULT_ADMIN_EMAIL
from api.model.role import Role
from api.model.db import db

users_api = Blueprint("users", __name__)


@users_api.route("/", methods=["GET"])
@security_level_required(100)
def getUsers():
    """Get all users.

    Returns:
        all_users (json): List of all users in the database as user objects.
    """
    return jsonify(user_schema.dump(User.query.filter_by(deprecated=False))), 200


@users_api.route("/<id>", methods=["DELETE"])
@security_level_required(100)
def deleteUser(id, current_user):
    """Delete a single user.

    Args:
        id (int): the id of the user to be deleted.

    Returns:
        user (json): Deleted user as a user objects.
    """

    user = User.query.filter_by(id=id)

    res = single_user_schema.dump(user.first())

    if res["email"].lower() == DEFAULT_ADMIN_EMAIL:
        return jsonify({"message": "Cannot delete default admin."}), 405

    user.first().deprecated = True
    db.session.commit()

    role = Role.query.filter_by(role_id=res["role_id"]).first()

    # Logs the user deletion
    audit.recordDelete(res["email"], role.name, current_user["email"])

    return jsonify(res), 200


@users_api.route("/", methods=["PATCH"])
@required_parameters(["first_name", "last_name"])
@security_level_required(25)
def updateUserDetails(current_user):
    """Updates the user's first and last name.

    Returns:
        response (json): Success message.
    """
    data = request.get_json()

    user = UserName.query.filter_by(user_id=current_user["id"]).first()
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]

    db.session.commit()
    return jsonify({"message": "Update successful."}), 200


@users_api.route("/password", methods=["PATCH"])
@required_parameters(["current_password", "new_password", "confirm_password"])
@security_level_required(25)
def updatePassword(current_user):
    """Updates the user's password.

    Returns:
        response (json): Success message.
    """
    data = request.get_json()

    # Validates password fields
    if len(data["new_password"].strip()) == 0:
        return jsonify({"message": "Password cannot be blank."}), 400

    user = User.query.filter_by(id=current_user["id"]).first()
    if not check_password_hash(user.password, data["current_password"]):
        return jsonify({"message": "Incorrect password"}), 400

    if data["new_password"] != data["confirm_password"]:
        return jsonify({"message": "New passwords do not match."}), 400

    if data["current_password"] == data["new_password"]:
        return jsonify({"message": "Cannot change password to itself."}), 400

    user.password = generate_password_hash(
        data["new_password"], method="sha256")

    db.session.commit()
    return jsonify({"message": "Update successful. "}), 200


@users_api.route("/role", methods=["PATCH"])
@required_parameters(["user_id", "role_id"])
@security_level_required(100)
def updateUserRole(current_user):
    """"Changes the role of a user.

    Returns:
        response (json): Success message.
    """

    data = request.get_json()

    if User.query.filter_by(id=data["user_id"]).first().email == DEFAULT_ADMIN_EMAIL:
        return jsonify({"message": "Cannot change role of default admin."}), 405

    user = User.query.filter_by(id=data["user_id"]).first()
    user.role_id = data["role_id"]

    db.session.add(user)
    db.session.commit()

    role = Role.query.filter_by(role_id=data["role_id"]).first()

    # Logs the user update
    audit.recordUpdate(user.email, role.name, current_user["email"])

    return jsonify({"message": "Updated user."}), 200
