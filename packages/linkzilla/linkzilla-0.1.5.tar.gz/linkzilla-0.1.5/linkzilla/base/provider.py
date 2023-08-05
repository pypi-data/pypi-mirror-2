import urllib2
from StringIO import StringIO
from gzip import GzipFile
import logging
import socket
import os
import shutil
import warnings
from traceback import format_exc

from linkzilla import get_storage
from linkzilla.settings import USER_AGENT, DEFAULT_TIMEOUT, DB_DELIMITER

warnings.filterwarnings('ignore', 'tmpnam')
socket.setdefaulttimeout(DEFAULT_TIMEOUT)


class BaseProvider(object):
    def __init__(self, config):
        self.config = config
        mod = get_storage(config['storage']['name'])
        self.storage = mod.Storage(config)

    def display_error(self, msg):
        """
        Display error message and dump exception traceback.
        """

        logging.error(msg)
        logging.error(format_exc())

    def fetch_remote_file(self, url):
        """
        Retreive remove file and save it locally.

        Args:
            url: absolute URL of remote file
            localpath: local path where file should be saved

        Return:
            Content of retreived file or None if somthing went wrong.
        """

        logging.debug(u'Fetching remote file from %s' % url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        req.add_header('Accept-Encoding', 'gzip')
        opener = urllib2.build_opener()

        try:
            response = opener.open(url)
        except Exception, ex:
            self.display_error(u'Error while opening remote database')
        else:
            if response.code == 200:
                data = response.read()
                logging.debug(u'Response headers: %s' % dict(response.headers))
                if 'gzip' in response.headers.get('Content-Encoding', ''):
                    data = GZipFile(fileobj=StringIO(data)).read()
                return data
            else:
                logging.error(u'Invalid response status: %d' % response.code)

        return None

    def fetch_database(self):
        """
        Return content of remote database.
        """

        raise NotImplemented()

    def refresh_local_database(self):
        """
        Fetch remote database, parse it and replace the local database.
        """

        data = self.fetch_database()
        if data:
            try:
                mapping = self.parse_database(data)
            except Exception, ex:
                self.display_error(u'Invalid database structure')
            else:
                logging.debug('Found %d items in dump' % len(mapping))
                self.save_database(mapping)


    def parse_database(self, data):
        """
        Parse the raw data fetched from service server.
        """

        raise NotImplemented()

    def save_database(self, mapping):
        """
        Save database in dbm file.

        Args:
            mapping: str -> (str,)
        """

        try:
            self.storage.update(mapping)
        except Exception, ex:
            self.display_error(u'Error while saving database: %s' % ex)


    def read_database_key(self, key):
        """
        Read the key value from database.

        If nothing was found return empty string.
        """

        return self.storage.read_key(key)
