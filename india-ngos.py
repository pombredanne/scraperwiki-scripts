"""List of NGOs registered in http://ngo.india.gov.in as part of Govt. of India's NGO partnership system
"""

import scraperwiki
import lxml.html

utils = scraperwiki.utils.swimport("utils")


def get_states():
    url = 'http://ngo.india.gov.in/ngo_stateschemes_ngo.php'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    assert 'sect_key' in html
    links = root.cssselect('a[href*=sect_key]') # States have sect_key in href
    return [link.get('href').split("'")[1] for link in links]


def get_ngo_urls(states):
    ngos = []
    for state in states:
        url = 'http://ngo.india.gov.in/state_ngolist_ngo.php?records=99999&state_value=' + state
        print "Processing", url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        assert 'view_ngo' in html
        links = root.cssselect('a[href*=view_ngo]') # NGOs have view_ngo in href
        ngos.extend([link.get('href').split("'")[1] for link in links])
    return ngos


@utils.cache
def get_ngo_details(ngo):
    url = 'http://ngo.india.gov.in/view_ngo_details_ngo.php?ngo_id=' + ngo
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    td = root.cssselect('td .hm_section_head_bg1')[0]
    rows = list(td.getparent().itersiblings())
    rec = dict()
    rec['ngo_id'] = ngo
    rec['ngo_name'] = td.text_content().split(':')[-1]

    for row in rows:
        cells = row.cssselect('td')
        if len(cells) != 4:
            # There are some empty rows
            continue

        name = cells[1].text_content()
        value = cells[3].text_content()
        if name and value:
            rec[name] = value

    utils.save(rec, ['ngo_id'])


@utils.clear_cache
def main():
    states = get_states()
    ngos = get_ngo_urls(states)
    for ngo in sorted(set(ngos)):
        get_ngo_details(ngo)


main()
