try:
    import cPickle as pickle
except ImportError:
    import pickle

from linkzilla.base.client import BaseClient
from linkzilla.services.linkfeed.provider import Provider

class Client(BaseClient):
    def load_links(self, key):
        provider = Provider(self.config)
        read = lambda x: provider.read_database_key(x)
        links = read(key)
        config = pickle.loads(read('config_config')[0].encode('utf-8'))
        items = []

        # hack...
        if not links:
            links = [None]

        for link in links:
            html = []
            html.append(config['start'])
            if link:
                html.append(config['before_text'])
                html.append(link)
                if links[-1] != link:
                    html.append(config['delimiter'])
                html.append(config['after_text'])
            html.append(config['end'])
            items.append(''.join(html))
        return items


if __name__ == '__main__':
    client = Client('/tmp/links.db', 'five')
    print client.next_links(1)
    print client.next_links(2)
    print client.next_links(10)
