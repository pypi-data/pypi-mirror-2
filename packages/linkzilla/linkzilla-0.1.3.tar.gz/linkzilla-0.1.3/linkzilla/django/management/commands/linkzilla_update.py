import logging

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from linkzilla import get_service

class Command(BaseCommand):
    help = 'Refresh local database containing cached links'

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)

        # Clear storage
        # TODO: change linkzilla settings: make only one storage config
        # outside the service configs

        providers = []
        for service_name in settings.LINKZILLA_SERVICES:
            service = get_service(service_name)
            config = settings.LINKZILLA_CONFIG[service_name]
            provider = service.Provider(config)
            providers.append(provider)

        for provider in providers:
            provider.storage.clear()

        for provider in providers:
            provider.refresh_local_database()
