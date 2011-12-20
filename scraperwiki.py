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
    def save(self, data=[], unique_keys=[]):
        pprint(data)

sqlite = sqlite1()
