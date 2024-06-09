from functools import wraps
from flask import request, jsonify


def required_parameters(parameters=[]):
    """Decorator that checks whether all parameters are provided in the body for a request.

    Args:
        parameters (list, optional): holds all the parameters to be checked. Defaults to [].
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            if not (request.content_type and request.content_type.startswith("application/json")):
                return jsonify({"message": "Invalid content type."}), 415

            data = request.get_json()

            # Checks each parameter provided
            for param in parameters:
                if param not in data:
                    return jsonify({"message": f"Missing required parameter: {param}."}), 400

            return f(*args, **kw)
        return wrapper
    return decorator
