from flask import Blueprint, jsonify, request, current_app
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from api.route.roles import security_level_required
from api.utils.validation import required_parameters
from email.utils import parseaddr
from api.model.user import User
from api.model.user_name import UserName
from api.model.role import Role
from functools import wraps
from api.model.db import db
import api.utils.userAudit as audit
import jwt

auth_api = Blueprint("auth", __name__)


def validate_params(f):
    """Decorator for validating the email and password."""
    @wraps(f)
    def wrapper(*args, **kw):

        data = request.get_json()

        if data["email"].strip() == "":
            return jsonify({"message": "Email cannot be empty."}), 400

        if data["password"].strip() == "":
            return jsonify({"message": "Password cannot be empty."}), 400

        # Check that email contains @, and doesn't start with @
        if "@" not in parseaddr(data["email"])[1] or data["email"].strip()[0] == "@":
            return jsonify({"message": "Invalid email address."}), 400

        return f(*args, **kw)
    return wrapper


@auth_api.route("/register", methods=["POST"])
@required_parameters(["email", "password"])
@validate_params
@security_level_required(100)
def register(current_user):
    """
    Registers a new user and stores them in the database.

    Returns:
        response (json): New user email and success message.
    """
    data = request.get_json()

    # If the email address is already in use
    if User.query.filter_by(email=data["email"].lower()).first() != None:
        return jsonify({"message": "Account with email address already exists."}), 400

    user = User(data["email"].strip().lower(),
                data["password"], data["role_id"])
    db.session.add(user)
    db.session.flush()
    db.session.refresh(user)

    # Sets first part of email and "User" as the first and last name
    user_name = UserName(data["email"].split("@")[0], "User", user.id)
    db.session.add(user_name)
    db.session.commit()

    role = Role.query.filter_by(role_id=data["role_id"]).first().name

    # Logs the user creation
    audit.recordCreate(data["email"].strip().lower(),
                       role, current_user["email"])

    return jsonify({
        "message": "User created.",
        "user": {
            "email": user.email
        }
    }), 201


@auth_api.route("/login", methods=["POST"])
@required_parameters(["email", "password"])
@validate_params
def login():
    """
    Authenticates the user if they provide the correct credentials.

    Returns:
        user (json): A JSON containing a JWT token and the user's details.
    """
    data = request.get_json()

    # Checks whether email and password are correct
    user = User.query.filter_by(email=data["email"].lower()).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Incorrect email address or password."}), 401

    #Checks whether user is deprecated
    if user.deprecated:
        return jsonify({"message":"Invalid user"}), 401

    user_role = Role.query.filter_by(role_id=user.role_id).first()
    user_details = UserName.query.filter_by(user_id=user.id).first()

    # Sets the token
    token = jwt.encode({
        "id": user.id,
        "email": user.email,
        "role": user_role.name,
        "exp": datetime.utcnow() + timedelta(minutes=30)},
        current_app.config["SECRET_KEY"])

    return jsonify({
        "id": user.id,
        "message": "Login Successful.",
        "token": token,
        "email": user.email,
        "role": user_role.name,
        "level": user_role.security_level,
        "fname": user_details.first_name,
        "lname": user_details.last_name
    }), 200
