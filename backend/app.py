from dotenv import load_dotenv
from os import getenv
from flask import Flask
from api.route.assets import asset_api
from api.route.roles import role_api
from api.route.assetTypes import asset_types_api
from api.route.auth import auth_api
from api.route.tags import tag_api
from api.route.users import users_api
from api.route.audit import audit_api
from api.model.db import db
from api.route.project import project_api
from api.route.comments import comment_api
import jobs


def create_app(Testing=False):
    """
    Initialises the app.

    Args:
        Testing (boolean): False when the app is run, True when tests are run

    Returns:
        app (Flask): the app after it has been successfully set up
    """
    app = Flask(__name__)

    # Determines database used
    if Testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = getenv("TEST_DATABASE_URI")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
            "SQLALCHEMY_DATABASE_URI")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS").lower() in "true"
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")

    db.init_app(app)

    # Sets blueprints for routes
    app.register_blueprint(asset_types_api, url_prefix="/asset/type")
    app.register_blueprint(asset_api, url_prefix="/asset")
    app.register_blueprint(auth_api, url_prefix="/auth")
    app.register_blueprint(tag_api, url_prefix="/tag")
    app.register_blueprint(role_api, url_prefix="/role")
    app.register_blueprint(users_api, url_prefix="/user")
    app.register_blueprint(project_api, url_prefix="/project")
    app.register_blueprint(audit_api, url_prefix="/audit")
    app.register_blueprint(comment_api, url_prefix="/comment")

    return app


load_dotenv()

if __name__ == "__main__":
    app = create_app()

    # Sets initial app configurations
    with app.app_context():
        jobs.run()

    app.run(debug=getenv("DEBUG").lower() in "true", port=getenv("FLASK_PORT"))
