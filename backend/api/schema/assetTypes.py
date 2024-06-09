from api.schema.ma import ma
from api.model.assetTypes import AssetType, AssetTypeAttribute
from api.schema.users import UserSchema


class TypeSchema(ma.Schema):
    """Schema for getting the type of asset type attributes."""
    class Meta:
        fields = ("type_name", "type_id")


type_schema = TypeSchema(many=True)
single_type_schema = TypeSchema(many=False)


class AssetTypeAttributeSchema(ma.Schema):
    """Schema for getting all attributes of an asset type."""
    class Meta:
        model = AssetTypeAttribute
        fields = ("asset_attribute_id", "asset_type_id",
                  "attribute_name", "attribute_type_id")

        attribute_type = ma.Nested(TypeSchema(many=False))


asset_type_attribute_schema = AssetTypeAttributeSchema(many=True)
single_asset_type_attribute_schema = AssetTypeAttributeSchema(many=False)


class AssetTypeSchema(ma.Schema):
    """Schema for getting all data of an asset type."""
    class Meta:
        model = AssetType
        fields = ("asset_type_id", "asset_type_name", "created_on",
                  "last_updated", "attributes", "created_by", "inherited_from")

    attributes = ma.List(ma.Nested(AssetTypeAttributeSchema()))
    created_by = ma.Nested(UserSchema())


asset_type_schema = AssetTypeSchema(many=True)
single_asset_type_schema = AssetTypeSchema(many=False)


class AssetBasicInfoSchema(ma.Schema):
    """Schema for getting only the id and name of an asset type."""
    class Meta:
        model = AssetType
        fields = ("asset_type_id", "asset_type_name")


asset_type_info_schema = AssetBasicInfoSchema(many=True)
single_asset_type_info_schema = AssetBasicInfoSchema(many=False)
