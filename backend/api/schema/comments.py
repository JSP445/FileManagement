from api.schema.ma import ma
from api.schema.users import UserSchema


class CommentIdSchema(ma.Schema):
    """Schema for getting the id of a comment."""
    class Meta:
        fields = ("id",)


class CommentSchema(ma.Schema):
    """Schema for getting all data of a comment."""
    class Meta:
        fields = ("id", "message", "reply_to", "created_by", "created_on")

    created_by = ma.Nested(UserSchema())
    reply_to = ma.Nested(CommentIdSchema())


comment_schema = CommentSchema(many=True)
single_comment_schema = CommentSchema(many=False)
