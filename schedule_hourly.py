# Runs certain scrapers on hourly basis

import mechanize
import cofre

scrapers = "india_weather_observations india_ngos"
urls = ["https://scraperwiki.com/scrapers/schedule-scraper/%s/run/" % scraper for scraper in scrapers.split()]

br = mechanize.Browser()

def login():
    br.open("https://scraperwiki.com/login/")
    br.select_form(nr=0)
    br['user_or_email'] = username = cofre.get('scraperwiki_username')
    br['password'] = cofre.get('scraperwiki_password')
    br.submit()


def main():
    login()
    for url in urls:
        br.open(url)
        print url, br.response().read()


main()
