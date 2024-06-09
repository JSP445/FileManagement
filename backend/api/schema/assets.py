from api.schema.ma import ma
from api.schema.users import UserSchema
from api.schema.projects import ProjectSchema
from api.schema.tags import TagSchema
from api.schema.assetTypes import AssetBasicInfoSchema, AssetTypeAttributeSchema


class AssetAttributeSchema(ma.Schema):
    """Schema for getting all attributes of an asset."""
    class Meta:
        fields = ('asset_attribute_id', 'attribute_value',
                  'asset_id', 'asset_attribute_type_id', 'attribute_name')
    attribute_name = ma.Nested(AssetTypeAttributeSchema())


asset_attribute_schema = AssetAttributeSchema(many=True)
single_asset_attribute_schema = AssetAttributeSchema(many=False)


class AssetSchema(ma.Schema):
    """Schema for getting all data of an asset."""
    class Meta:
        fields = ("asset_id", "asset_name", "asset_type_id",
                  "created_on", "attribute_values", "created_by")
    attribute_values = ma.List(ma.Nested(AssetAttributeSchema()))
    created_by = ma.Nested(UserSchema())


asset_schema = AssetSchema(many=True)
single_asset_schema = AssetSchema(many=False)


class AdvancedAssetSchema(ma.Schema):
    """Schema for getting all data of an asset and its relations."""
    class Meta:
        fields = ("asset_id", "asset_name", "asset_type_id",
                  "created_on", "created_by",  "last_updated", "attribute_values", "tags", "projects", "asset_type")

    created_by = ma.Nested(UserSchema)
    attribute_values = ma.List(ma.Nested(AssetAttributeSchema()))
    tags = ma.List(ma.Nested(TagSchema()))
    projects = ma.List(ma.Nested(ProjectSchema()))
    asset_type = ma.Nested(AssetBasicInfoSchema())


single_advanced_asset_schema = AdvancedAssetSchema(many=False)
advanced_asset_schema = AdvancedAssetSchema(many=True)
