from api.model.userAudit import UserAudit
from datetime import datetime
from api.model.db import db


def __record(subject, subject_role, admin, operation):
    """Records the log of a change to a user into the database.

    Args:
        subject (str): the email of the user being modified.
        subject_role (str): the role of the user being modified.
        admin (str): the email of the admin user modifying the user.
        operation (str): the modification performed on the user.
    """
    log = UserAudit(subject, subject_role, admin, operation, datetime.now())
    db.session.add(log)
    db.session.commit()


def recordCreate(subject, subject_role, admin):
    """Adds a record for creating a new user."""
    __record(subject, subject_role, admin, "CREATE")


def recordDelete(subject, subject_role, admin):
    """Adds a record for updating a user's role."""
    __record(subject, subject_role, admin, "DELETE")


def recordUpdate(subject, subject_role, admin):
    """Adds a record for deleting a user."""
    __record(subject, subject_role, admin, "UPDATE")
