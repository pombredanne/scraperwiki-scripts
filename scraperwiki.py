"""Fake module to test ScraperWiki scripts locally
"""

from pprint import pprint
import requests


def scrape(url, params=None):
    if params:
        return requests.post(url, data=params).content
    else:
        return requests.get(url).content


class sqlite1:
    def save(self, data=[], unique_keys=[], table_name='', verbose=2):
        pprint(data)

    def execute(self, query):
        pass

    def select(self, query):
        pass


class utils1:
    def swimport(self, module):
        import utils
        return utils


sqlite = sqlite1()
utils = utils1()
