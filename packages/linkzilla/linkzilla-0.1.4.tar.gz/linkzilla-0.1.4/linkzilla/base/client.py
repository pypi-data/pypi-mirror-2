import itertools
import logging

class BaseClient(object):
    def __init__(self, url, config):
        """
        Args:
            path: path to local database file
            url: the *escaped* url of site page for which links should be
                extracted from local database
        """

        self.config = config
        self.url = url
        self.error = ''

    def load_links(key):
        raise NotImplemented()

    def links(self):
        """
        Return all links on current page.
        """

        if not hasattr(self, '_links'):
            try:
                self._links = self.load_links(self.url)
            except Exception, ex:
                self._links = []
                self.error = unicode(ex)
                logging.error(u'sape: %s' % unicode(ex))
        return self._links


    def next_links(self, number=1):
        """
        Return next `number` links on current page.
        """

        if not hasattr(self, '_iterator'):
            self._iterator = itertools.chain(self.links())
        return list(itertools.islice(self._iterator, number))
