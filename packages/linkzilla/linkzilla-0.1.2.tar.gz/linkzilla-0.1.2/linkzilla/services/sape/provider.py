import anydbm

from linkzilla.base.provider import BaseProvider, DB_DELIMITER
from linkzilla.lib import phpserialize

REMOTE_DATABASE_PATH = '/code.php?user=%(user)s&host=%(host)s&charset=utf-8'
SAPE_SERVERS = ['dispenser-01.sape.ru', 'dispenser-02.sape.ru']

class Provider(BaseProvider):
    def build_database_url(self, user, client_host, sape_server):
        """
        Build absolute URL of remote file containing links.

        Args:
            user: sape.ru account ID
            host: hostname of the client site
        """

        path = REMOTE_DATABASE_PATH % ({'user': user, 'host': client_host})
        return 'http://%s%s' % (sape_server, path)

    def fetch_database(self):
        """
        Return content of remote database for given `user` and `host`.

        Args:
            user: sape.ru account ID
            host: hostname of the client site
        """

        for sape_server in SAPE_SERVERS:
            url = self.build_database_url(self.config['user'],
                                          self.config['host'], sape_server)
            data = self.fetch_remote_file(url)
            if data:
                if data.startswith('FATAL ERROR'):
                    logging.error(u'Sape.ru error: %s' % data)
                else:
                    return data
        return None

    def parse_database(self, data):
        """
        Parse the raw data fetched from sape.ru server.
        """

        links = {}
        dump = phpserialize.loads(data)
        for key, value in dump.iteritems():
            if isinstance(value, dict):
                value = value.values()
            else:
                value = [value]
            links[key] = value
        return links
