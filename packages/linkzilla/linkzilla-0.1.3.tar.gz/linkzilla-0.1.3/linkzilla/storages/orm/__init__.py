from linkzilla.base.storage import BaseStorage

from linkzilla.storages.orm.models import Item

class Storage(BaseStorage):
    def clear(self):
        Item.objects.all().delete()

    def update(self, mapping):
        """
        Clear storage and save new key/values.
        """

        for key, value in mapping.iteritems():
            key = self.build_key(key)
            value = self.pack_value(value)
            item, new = Item.objects.get_or_create(key=key, defaults={'value': value})
            if new:
                item.value = value
                item.save()

    def _read_key(self, key):
        """
        If nothing was found return empty string.
        """

        try:
            value = Item.objects.get(key=key).value
        except Item.DoesNotExist:
            value = None
        return value
