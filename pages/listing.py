from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Listing(object):

    ID_POSTINGBODY = 'postingbody'

    def __init__(self, link='https://losangeles.craigslist.org/wst/apa/d/live-on-sailboat/6481486080.html'):
        self.link = link
        page = urlopen(link)
        soup = BeautifulSoup(page.read(), "html.parser")
        print(page.read())

    def get(self):
        pass

    def parse_body(self):
        pass

