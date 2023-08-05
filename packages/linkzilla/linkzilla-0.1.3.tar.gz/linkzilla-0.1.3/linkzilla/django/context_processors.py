import urllib

from django.conf import settings

from linkzilla import get_service

def linkzilla(request):
    if not hasattr(request, '_linkzilla_links'):
        path = urllib.quote(request.path.encode('utf-8'), safe='/')
        qs = request.META.get('QUERY_STRING', '')
        if qs:
            path += '?' + qs

        links = []

        for service_name in settings.LINKZILLA_SERVICES:
            service = get_service(service_name)
            client = service.Client(path, settings.LINKZILLA_CONFIG[service_name])
            links.extend(client.links())

        request._linkzilla_links = links

    return {'linkzilla': {'all':  request._linkzilla_links}}
