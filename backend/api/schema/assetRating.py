from api.schema.ma import ma


class RatingSchema(ma.Schema):
    """Schema for finding association between assets."""
    class Meta:
        fields = ("asset_id", "rating")
        ordered = True


ratings_schema = RatingSchema(many=True)
