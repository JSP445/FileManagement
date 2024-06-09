from api.model.user import User
from api.model.user_name import UserName
from api.model.role import Role
from api.model.db import db
from api import DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD


def default_admin():
    """Adds the default admin user into the database."""
    if not User.query.filter_by(email=DEFAULT_ADMIN_EMAIL).first():
        role = Role.query.filter_by(name="Admin").first()
        user = User(DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD, role.role_id)
        user.id = 0
        db.session.add(user)
        db.session.flush()
        db.session.refresh(user)

        username = UserName("System", "Admin", user.id)
        db.session.add(username)
        db.session.commit()
