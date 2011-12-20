"""List of various Indian National Award Winners
"""
from datetime import datetime
import re
from pprint import pprint
import scraperwiki
import lxml.html

base_url = 'http://india.gov.in/myindia/'
awards = dict()


def get_awards_list():
    url = base_url + 'advsearch_awards.php'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    options = root.cssselect('form[name=frm2] select[name=award] option')
    for option in options:
        id = option.get('value')
        if not id:
            continue
        name = option.text_content()
        awards[id] = name


def get_awardees():
    for award in awards:
        for i in range(100000):
            url = base_url + 'awards.php?type=%s&start=%s' % (award, i*10)
            print "Processing", url
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            items = root.cssselect('div.awardsblock1 ul li')

            #from IPython import embed
            #embed()

            if not items:
                break

            data = []
            for item in items:
                rec = dict()
                meta = item.cssselect('span')[0]
                item.remove(meta)

                meta_data = meta.text_content().split(' : ')

                name = item.text_content()
                name = ' '.join(name.split()) # Remove extra whitespace
                rec['awardee_name'] = name
                rec['award_code'] = award
                rec['award_name'] = awards[award]
                rec['state'] = meta_data[-1]
                rec['year'] = meta_data[-2]
                if len(meta_data) == 3:
                    rec['area'] = meta_data[-3]
                rec['crawled_on'] = datetime.now()
                data.append(rec)

            scraperwiki.sqlite.save(data=data, unique_keys=['award_code', 'year', 'awardee_name'])


get_awards_list()
get_awardees()
