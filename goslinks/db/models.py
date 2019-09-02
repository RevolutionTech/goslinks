from pynamodb.attributes import UnicodeAttribute


class UserModel:
    class Meta:
        table_name = "goslinks-users"
        read_capacity_units = 1
        write_capacity_units = 1

    email = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    photo = UnicodeAttribute()

    @property
    def organization(self):
        _, o = self.email.split("@")
        return o

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


class LinkModel:
    class Meta:
        table_name = "goslinks-links"
        read_capacity_units = 1
        write_capacity_units = 1

    name = UnicodeAttribute(hash_key=True)  # contains organization name and link name
    url = UnicodeAttribute()
    owner = UnicodeAttribute()

    @staticmethod
    def name_from_organization_and_slug(organization, slug):
        return f"{organization}|{slug}"

    @classmethod
    def get_from_organization_and_slug(cls, organization, slug, **kwargs):
        name = cls.name_from_organization_and_slug(organization, slug)
        return cls.get(hash_key=name, **kwargs)

    @classmethod
    def get_or_init(cls, user, slug):
        name = cls.name_from_organization_and_slug(user.organization, slug)
        try:
            link = cls.get(name)
        except cls.DoesNotExist:
            link = cls(name=name)

        link.owner = user.email
        return link

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
