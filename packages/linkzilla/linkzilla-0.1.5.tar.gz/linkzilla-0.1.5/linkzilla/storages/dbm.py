import anydbm

from linkzilla.base.storage import BaseStorage

class Storage(BaseStorage):
    def clear(self):
        db = anydbm.open(self.config['storage']['database_path'], 'n')

    def update(self, mapping):
        """
        Clear storage and save new key/values.
        """

        db = anydbm.open(self.config['storage']['database_path'], 'c')
        for key, value in mapping.iteritems():
            db[self.build_key(key)] = self.pack_value(value)

    def _read_key(self, key):
        """
        If nothing was found return empty string.
        """

        if not hasattr(self, 'db'):
            self.db = anydbm.open(self.config['storage']['database_path'], 'c')
        try:
            value = self.db[key]
        except KeyError:
            value = None
        return value
