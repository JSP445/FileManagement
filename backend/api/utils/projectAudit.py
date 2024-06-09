from api.model.projectAudit import ProjectAudit
from datetime import datetime
from api.model.db import db


def __record(project_name, user_email, operation, description=None):
    """Records the log of a change to a project into the database.

    Args:
        project_name (str): the name of the project being modified.
        user_email (str): the email of the user modifying the project.
        operation (str): the modification performed on the project.
        description (str, optional): a description of the modification perfomed. Defaults to None.
    """
    log = ProjectAudit(project_name, user_email, operation,
                       datetime.now(), description)
    db.session.add(log)
    db.session.commit()


def recordCreate(project_name, user_email):
    """Adds a record for creating a new project."""
    __record(project_name, user_email, "CREATE")


def recordUpdate(project_name, user_email, names):
    """Adds a record for updating a project.

    Args:
        names (tuple): contains the project name before and after the update.
    """
    if names[0] != names[1]:
        description = f"{names[0]} renamed to {names[1]}"
        __record(project_name, user_email, "UPDATE", description)
    else:
        __record(project_name, user_email, "UPDATE")


def recordDelete(project_name, user_email):
    """Adds a record for deleting a project."""
    __record(project_name, user_email, "DELETE")
