import pynamodb.exceptions as pynamodb_exceptions
from pynamodb.attributes import AttributeContainer


class FakeModel(AttributeContainer):
    """
    FakeModel attempts to replicate the interface
    of pynamodb.models.Model, with an in-memory backend.

    However, only the methods (and functionality)
    actually used by goslinks are implemented.
    """

    _data = None

    DoesNotExist = pynamodb_exceptions.DoesNotExist

    def __init__(self, hash_key=None, range_key=None, **attributes):
        if range_key is not None:
            raise NotImplementedError

        if hash_key is not None:
            attributes[self._get_hash_keyname()] = hash_key

        super().__init__(**attributes)

    @classmethod
    def _get_hash_keyname(cls):
        for keyname, attribute in cls._attributes.items():
            if attribute.is_hash_key:
                return keyname

        raise NotImplementedError

    @classmethod
    def count(cls, hash_key=None, **kwargs):
        if hash_key is None or kwargs or cls._data is None:
            raise NotImplementedError

        return int(hash_key in cls._data)

    @classmethod
    def create_table(cls, **kwargs):
        if kwargs:
            raise NotImplementedError

        cls._data = {}

    @classmethod
    def delete_table(cls):
        cls._data = None

    @classmethod
    def exists(cls):
        return cls._data is not None

    @classmethod
    def get(cls, hash_key, **kwargs):
        if kwargs or cls._data is None:
            raise NotImplementedError

        try:
            return cls._data[hash_key]
        except KeyError:
            raise cls.DoesNotExist()

    def save(self, **kwargs):
        if kwargs or self._data is None:
            raise NotImplementedError

        hash_key = self.attribute_values[self._get_hash_keyname()]
        self._data[hash_key] = self
