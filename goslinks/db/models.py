from pynamodb.attributes import UnicodeAttribute


class UserModel(object):
    class Meta:
        table_name = "Users"
        host = "http://localhost:8000"
        read_capacity_units = 1
        write_capacity_units = 1

    email = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    photo = UnicodeAttribute()

    @classmethod
    def update_or_create_user(cls, user_info):
        email = user_info["email"]
        try:
            user = cls.get(email)
        except cls.DoesNotExist:
            user = cls(email)

        user.name = user_info["name"]
        user.photo = user_info["picture"]
        user.save()
        return user


class LinkModel(object):
    class Meta:
        table_name = "Links"
        host = "http://localhost:8000"
        read_capacity_units = 1
        write_capacity_units = 1

    name = UnicodeAttribute(hash_key=True)  # contains organization name and link name
    url = UnicodeAttribute()
    owner = UnicodeAttribute()

    @property
    def organization(self):
        o, _ = self.name.split("|")
        return o

    @property
    def slug(self):
        _, s = self.name.split("|")
        return s

    @property
    def owner_user(self):
        from goslinks.db.factory import get_model

        if not self.owner.endswith(self.organization):
            raise AssertionError(
                "Owner does not belong to the organization this link is contained in"
            )

        return get_model("user").get(self.owner)


MODEL_REGISTRY = {"user": UserModel, "link": LinkModel}
