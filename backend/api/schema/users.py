from api.schema.ma import ma


class UserNameSchema(ma.Schema):
    """Schema for getting the name of a user."""
    class Meta:
        fields = ("first_name", "last_name")


user_name_schema = UserNameSchema(many=True)
single_user_name_schema = UserNameSchema(many=False)


class UserSchema(ma.Schema):
    """Schema for getting the data of a user."""
    class Meta:
        fields = ("id", "email", "user_name", "role_id")

    user_name = ma.Nested(UserNameSchema())


user_schema = UserSchema(many=True)
single_user_schema = UserSchema(many=False)


class RoleSchema(ma.SQLAlchemySchema):
    """Schema for getting all data of a role."""
    class Meta:
        fields = ("role_id", "name", "security_level")


role_schema = RoleSchema(many=True)
single_role_schema = RoleSchema(many=False)
