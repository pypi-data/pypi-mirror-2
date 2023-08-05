Installation
============

Just install `linkzilla` package via easy_install, pip or from repository.

Repository URL: http://bitbucket.org/lorien/linkzilla


Usage in django project
=======================

 * Create directory where local links database should be saved
 * Put 'linkzilla.django' into settings.INSTALLED_APPS
 * Put 'linkzilla.django.context_processors.linkzilla'
   into settings.TEMPLATE_CONTEXT_PROCESSORS
 * Put service names to LINKZILLA_SERVICES. Enable which you want. On the moment
   only "sape" and "linkfeed" are supported
 * Put serivice configuration to LINKZILLA_CONFIG. Note that `host` parameter
   is duplicated in each section, it is simply your site hostname.

   Example:

        LINKZILLA_SERVICES = ['sape', 'linkfeed']
        LINKZILLA_CONFIG = {
            'sape': {
                'name': 'sape',
                'user': '...',
                'host': 'some.domain.com',
                'storage': {
                    'name': 'dbm',
                    'database_path': os.path.join(ROOT, 'var', 'linkzilla'),
                },
            },
            'linkfeed': {
                'name': 'linkfeed',
                'database_path': os.path.join(ROOT, 'var', 'sape.links'),
                'user': '...',
                'host': 'some.domain.com',
                'storage': {
                    'name': 'dbm',
                    'database_path': os.path.join(ROOT, 'var', 'linkzilla'),
                },
            },
        }

 * Setup cron to run periodically the command `manage.py linkzilla_update`.
   That command download fresh version of links database.
   Sample cron entry: * * * * * cd /web/project; ./manage.py linkzilla_update
 * Put `{{ linkzilla.all|safeseq|join:", " }} in the template




Usage in arbitrary python project
=================================

 * Write script which calls refresh_local_database method of each provider you use.
 * Call that script periodically with cron or anything else
 * To get all links for the URL use ``links`` method of client instance for each service you use.


TODO
====

Update the rest of documentation (below this line)


Example of Client usage
=======================

    from sape.client import Client

    url = 'http://mydomain.com/cat/subcat/?foo=bar'
    client = Client('var/links.db', url)
    links = client.links()


Example of Provider usage
=========================

    from sape.provider import refresh_local_database

    refresh_local_database('var/links.db', 'sape.ru ID', 'mydomain.com')
