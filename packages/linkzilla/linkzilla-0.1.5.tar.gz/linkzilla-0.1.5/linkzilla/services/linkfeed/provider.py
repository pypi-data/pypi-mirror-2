import anydbm
try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree
try:
    import cPickle as pickle
except ImportError:
    import pickle

from linkzilla.base.provider import BaseProvider, DB_DELIMITER
from linkzilla.lib import phpserialize

REMOTE_DATABASE_URL = 'http://db.linkfeed.ru/%(user)s/%(host)s/UTF-8.xml'

class Provider(BaseProvider):
    def build_database_url(self, user, client_host):
        """
        Build absolute URL of remote file containing links.

        Args:
            user: sape.ru account ID
            host: hostname of the client site
        """

        return REMOTE_DATABASE_URL % ({'user': user, 'host': client_host})

    def fetch_database(self):
        """
        Return content of remote database for given `user` and `host`.

        Args:
            user: sape.ru account ID
            host: hostname of the client site
        """

        url = self.build_database_url(self.config['user'], self.config['host'])
        data = self.fetch_remote_file(url)
        return data

    def parse_database(self, data):
        """
        Parse the raw data fetched from sape.ru server.
        """

        items = {}

        tree = ElementTree.fromstring(data)
        bot_ips = [x.text.encode('utf-8') for x in tree.findall('bot_ips/ip')]
        items['bot_ips'] = bot_ips

        config = {}
        for elem in tree.findall('config/item'):
            key = elem.get('name')
            config[key] = (elem.text or '').encode('utf-8')
            #items['config_%s' % key] = [(elem.text or '').encode('utf-8')]
        items['config_config'] = [pickle.dumps(config)]

        for page_node in tree.findall('pages/page'):
            page = items.setdefault(page_node.get('url'), [])
            for link_node in page_node.findall('link'):
                page.append(link_node.text.encode('utf-8'))

        return items


    #def read_database_key(self, key):
        #"""
        #Read the key value from database.

        #If key was not found try to read "__sape_new_url__" key.
        #If nothing was found return empty string.
        #"""

        #db = anydbm.open(self.config['database_path'])
        #try:
            #value = db[key]
        #except KeyError:
            #value = db.get('__sape_new_url__', '')
        #value = value.split(DB_DELIMITER)
        #return value
