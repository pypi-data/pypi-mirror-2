from linkzilla.settings import DB_DELIMITER

class BaseStorage(object):
    def __init__(self, config):
        self.config = config

    def read_key(self, key):
        """
        If nothing was found return empty string.
        """

        key = self.build_key(key)
        value = self._read_key(key)
        if value:
            value = self.unpack_value(value)
        else:
            value = []
        return value

    def pack_value(self, value):
        return DB_DELIMITER.join(value)

    def unpack_value(self, value):
        return value.split(DB_DELIMITER)

    def build_key(self, key):
        return '%s_%s' % (self.config['name'], key)

    # Interface methods

    def update(self, mapping):
        """
        Clear storage and save new key/values.
        """

        raise NotImplemented()

    def _read_key(self, key):
        """
        If nothing was found return empty string.
        """

        raise NotImplemented()

    def clear(self):
        """
        Clear database.
        """

        raise NotImplemented()
