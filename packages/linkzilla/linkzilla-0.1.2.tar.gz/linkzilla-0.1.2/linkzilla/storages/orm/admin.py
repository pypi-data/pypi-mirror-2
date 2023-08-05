from django.contrib import admin

from linkzilla.storages.orm.models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ['url', 'service']
    search_fields = ['key']

    def url(self, obj):
        return obj.key.split('_', 1)[1]

    def service(self, obj):
        return obj.key.split('_', 1)[0]

admin.site.register(Item, ItemAdmin)
