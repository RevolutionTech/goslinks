from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class UserModel(Model):
    class Meta:
        table_name = "Users"
        host = "http://localhost:8000"
        read_capacity_units = 1
        write_capacity_units = 1

    email = UnicodeAttribute(hash_key=True)


class LinkModel(Model):
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
        if not self.owner.endswith(self.organization):
            raise AssertionError(
                "Owner does not belong to the organization this link is contained in"
            )

        return UserModel.get(self.owner)
