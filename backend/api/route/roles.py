from flask import Blueprint, jsonify, request, current_app
from api.model.role import Role
from api.schema.users import role_schema
from api.model.user import User
from functools import wraps
import inspect
import jwt

role_api = Blueprint("role", __name__)


def security_level_required(level):
    """Decorator for restricting access to backend routes.

    Args:
        level (int): the required security level for accessing the route.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            auth_headers = request.headers.get("Authorization", "").split()
            invalid_msg = {"message": "Invalid token."}

            if len(auth_headers) != 2:
                return jsonify(invalid_msg), 401

            try:
                token = auth_headers[1]
                data = jwt.decode(
                    token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Expired token."}), 401

            except jwt.InvalidTokenError:
                return jsonify(invalid_msg), 401

            except Exception:
                return jsonify(invalid_msg), 500

            user = User.query.filter_by(email=data["email"]).first()

            if not user:
                return jsonify({"message": "User not found."}), 401

            security_level = Role.query.filter_by(
                role_id=user.role_id).first().security_level

            if security_level < level:
                return jsonify({
                    "message": "Access Denied. User does not have required permissions."}), 401

            # Provides current user's details to a route the decorator is used on if it is a requested parameter.
            if "current_user" in inspect.getfullargspec(f).args:
                kw["current_user"] = data

            return f(*args, **kw)
        return wrapper
    return decorator


@role_api.route("/", methods=["GET"])
@security_level_required(25)
def getRoles():
    """Gets all roles.

    Returns:
        all_roles (json): List of all roles in the database as role objects.
    """
    return jsonify(role_schema.dump(Role.query.all())), 200
