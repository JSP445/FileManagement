from api.model.assetAudit import AssetAudit
from datetime import datetime
from api.model.db import db


def __record(asset_name, user_email, operation, description=None):
    """Records the log of a change to an asset into the database.

    Args:
        asset_name (str): the name of the asset being modified.
        user_email (str): the email of the user modifying the asset.
        operation (str): the modification performed on the asset.
        description (str, optional): a description of the modification performed. Defaults to None.
    """
    log = AssetAudit(asset_name, user_email, operation,
                     datetime.now(), description)
    db.session.add(log)
    db.session.commit()


def recordCreate(asset_name, user_email):
    """Adds a record for creating a new asset."""
    __record(asset_name, user_email, "CREATE")


def recordUpdate(asset_name, user_email, names):
    """Adds a record for updating an asset.

    Args:
        names (tuple): contains the asset name before and after the update.
    """
    if names[0] != names[1]:
        description = f"{names[0]} renamed to {names[1]}"
        __record(asset_name, user_email, "UPDATE", description)
    else:
        __record(asset_name, user_email, "UPDATE")


def recordDelete(asset_name, user_email):
    """Adds a record for deleting an asset."""
    __record(asset_name, user_email, "DELETE")
