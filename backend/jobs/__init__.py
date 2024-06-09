from jobs.dbSetup import setup_database, setup_roles, setup_attribute_types, setup_default_asset_type
from jobs.defaultUsers import default_admin


def run():
    """Runs the methods that setup the initial database structure."""
    setup_database()
    setup_roles()
    default_admin()
    setup_attribute_types()
    setup_default_asset_type()
