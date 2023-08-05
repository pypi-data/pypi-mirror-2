from linkzilla.base.client import BaseClient
from linkzilla.services.sape.provider import Provider

class Client(BaseClient):
    def load_links(self, key):
        provider = Provider(self.config)
        links = provider.read_database_key(key)
        if links:
            return links
        else:
            return provider.read_database_key('__sape_new_url__')


if __name__ == '__main__':
    client = Client('/tmp/links.db', 'five')
    print client.next_links(1)
    print client.next_links(2)
    print client.next_links(10)
