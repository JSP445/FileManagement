from api.schema.ma import ma
from api.schema.users import UserSchema


class ProjectAssetSchema(ma.Schema):
    """Schema for getting specific data of an asset."""
    class Meta:
        fields = ("asset_id", "asset_name", "asset_type_id", "created_on")


class ProjectSchema(ma.Schema):
    """Schema for getting all data of a project."""
    class Meta:
        fields = ("project_id", "project_name",
                  "project_description", "assets", "created_by", "created_on")

    assets = ma.List(ma.Nested(ProjectAssetSchema()))
    created_by = ma.Nested(UserSchema)


project_schema = ProjectSchema(many=True)
single_project_schema = ProjectSchema(many=False)
