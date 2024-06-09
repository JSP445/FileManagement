from api.schema.ma import ma


class TagsAssetSchema(ma.Schema):
    """Schema for getting specific data of an asset."""
    class Meta:
        fields = ("asset_id", "asset_name", "asset_type_id", "created_on")


class TagNameSchema(ma.Schema):
    """Schema for getting the name of a tag."""
    class Meta:
        fields = ("tag_name",)


tag_name_schema = TagNameSchema(many=True)
single_tag_name_schema = TagNameSchema(many=False)


class TagSchema(ma.Schema):
    """Schema for getting the id and name of a tag."""
    class Meta:
        fields = ("tag_id", "tag_name")


single_tag_schema = TagSchema(many=False)
tag_schema = TagSchema(many=True)


class AdvancedTagSchema(ma.Schema):
    """Schema for getting the basic tag data and its assets."""
    class Meta:
        fields = ("tag_id", "tag_name", "assets")

    assets = ma.List(ma.Nested(TagsAssetSchema()))


advanced_tag_schema = AdvancedTagSchema(many=True)
single_advanced_tag_schema = AdvancedTagSchema(many=False)
