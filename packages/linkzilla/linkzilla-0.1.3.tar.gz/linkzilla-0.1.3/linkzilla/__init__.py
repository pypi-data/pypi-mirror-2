SERVICES = {}
STORAGES = {}

def get_service(name):
    if not name in SERVICES:
        SERVICES[name] = __import__('linkzilla.services.%s' % name, globals(), locals(), ['foo'])
    return SERVICES[name]


def get_storage(name):
    if not name in STORAGES:
        STORAGES[name] = __import__('linkzilla.storages.%s' % name, globals(), locals(), ['foo'])
    return STORAGES[name]
