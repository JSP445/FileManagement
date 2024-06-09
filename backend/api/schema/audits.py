from api.schema.ma import ma


class UserAuditSchema(ma.Schema):
    """Schema for getting all data of a change to a user."""
    class Meta:
        fields = ("id", "subject", "subject_role",
                  "admin", "operation", "time")


user_audit_schema = UserAuditSchema(many=True)
single_user_audit_schema = UserAuditSchema(many=False)


class AssetTypeAuditSchema(ma.Schema):
    """Schema for getting all data of a change to an asset type."""
    class Meta:
        fields = ("id", "asset_type_name", "email",
                  "operation", "time", "description")


asset_type_audit_schema = AssetTypeAuditSchema(many=True)
single_asset_type_audit_schema = AssetTypeAuditSchema(many=False)


class AssetAuditSchema(ma.Schema):
    """Schema for getting all data of a change to an asset."""
    class Meta:
        fields = ("id", "asset_name", "email",
                  "operation", "time", "description")


asset_audit_schema = AssetAuditSchema(many=True)
single_asset_audit_schema = AssetAuditSchema(many=False)


class ProjectAuditSchema(ma.Schema):
    """Schema for getting all data of a change to a project."""
    class Meta:
        fields = ("id", "project_name", "email",
                  "operation", "time", "description")


project_audit_schema = ProjectAuditSchema(many=True)
single_project_audit_schema = ProjectAuditSchema(many=False)
