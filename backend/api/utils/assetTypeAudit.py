from api.model.assetTypeAudit import AssetTypeAudit
from datetime import datetime
from api.model.db import db


def __record(asset_type_name, user_email, operation, description=None):
    """Records the log of a change to an asset type into the database.

    Args:
        asset_type_name (str): the name of the asset type being modified.
        user_email (str): the email of the user modifying the asset type.
        operation (str): the modification performed on the asset type.
        description (str, optional): a description of the modification performed. Defaults to None.
    """
    log = AssetTypeAudit(asset_type_name, user_email,
                         operation, datetime.now(), description)
    db.session.add(log)
    db.session.commit()


def recordCreate(asset_type_name, user_email):
    """Adds a record for creating a new asset type."""
    __record(asset_type_name, user_email, "CREATE")


def recordUpdate(asset_type_names, user_email):
    """Adds a record for updating an asset type.

    Args:
        asset_type_names (tuple): contains the asset type name before and after the update.
    """
    if asset_type_names[0] != asset_type_names[1]:
        description = f"{asset_type_names[0]} renamed to {asset_type_names[1]}"
        __record(asset_type_names[1], user_email, "UPDATE", description)
    else:
        __record(asset_type_names[1], user_email, "UPDATE")


def recordDelete(asset_type_name, user_email):
    """Adds a record for deleting an asset type."""
    __record(asset_type_name, user_email, "DELETE")
