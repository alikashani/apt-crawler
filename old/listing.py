from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import namedtuple


class Listing(object):

    MAP_ID = "map"
    LAT_TAG = "data-latitude"


    def __init__(self, info, geo_ranges=[]):
        id, title, time, link, price = info
        self.link = link
        page = urlopen(link)
        soup = BeautifulSoup(page.read(), "html.parser")
        lng, lat = self.get_cords(soup)

    def get_cords(self, soup):
        map = soup.find("div", {"id", self.MAP_ID})
        if map:
           return float(map.attrs['data-latitude']), float(map.attrs['data-longitude'])

        return '',''



#
# Listing = namedtuple('Listing', "id, title, time, link, price, lng, lat")

if __name__ == "__main__":
    #
    # test = Listing(id=1)
    # print(test)
    Listing(('','','','https://losangeles.craigslist.org/wst/apa/d/beautiful-3-bed-2-bath/6482040307.html',''))