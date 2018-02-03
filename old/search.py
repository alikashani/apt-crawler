from urllib.request import urlopen
from queue import Queue
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sqlite3


class SearchResults(object):
    
    BASE_URL = 'https://losangeles.craigslist.org'
    RESULTROW_CLASS = 'result-row'
    RESULTTITLE_CLASS = 'result-title'
    RESULTDATE_CLASS = 'result-date'
    RESULTPRICE_CLASS = 'result-price'
    RESULTIMAGE_CLASS = 'thumb'
    RANGETO_CLASS = 'rangeTo'
    TOTALCOUNT_CLASS = 'totalcount'
    NEXT_CLASS = 'next'

    def __init__(self, queue, db_name, link):
        self.queue = queue
        self.link = link
        self.min_time = datetime.now() - timedelta(1)
        self.conn = sqlite3.connect(db_name)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS listings
             (id integer primary key, title text, time text, link text, price integer)''')

    def run(self):
        page = urlopen(self.link)
        soup = BeautifulSoup(page.read(), "html.parser")
        self.get_info(soup)
        while self.has_next(soup):
            self.get_info(soup)
            next_link = self.BASE_URL + soup.find("a", {"class", self.NEXT_CLASS})['href']
            page = urlopen(next_link)
            soup = BeautifulSoup(page.read(), "html.parser")

    def get_info(self, soup):
        for row in soup.find_all("li", {"class", self.RESULTROW_CLASS}):
            try:
                id = int(row["data-pid"])
                time = row.find("time", {"class", self.RESULTDATE_CLASS})['datetime']
                title_info = row.find("a", {"class", self.RESULTTITLE_CLASS})
                link = title_info['href']
                title = title_info.text
                price = int(row.find("span", {"class", self.RESULTPRICE_CLASS}).text[1:])
                # save this for the time req
                self.last_seen_dt = self.to_datetime(time)
                if self.last_seen_dt > self.min_time:
                    self.queue.put((id, title, time, link, price))
            except Exception as e:
                print("ehhhh...", e)

    def has_next(self, soup):
        # Time Req
        if self.last_seen_dt < self.min_time:
            return False
        try:
            range_to = soup.find("span", {"class", self.RANGETO_CLASS}).text
            total = soup.find("span", {"class", self.TOTALCOUNT_CLASS}).text
            print(range_to, total)
            if int(range_to) < int(total):
                return True
        except:
            print("Done...")
        return False

    def to_datetime(self, time):
        return datetime.strptime(time, "%Y-%m-%d %H:%M")

    def save(self):
        pass



if __name__ == "__main__":
    queue = Queue()
    s = SearchResults(queue, 'apts.db', 'https://losangeles.craigslist.org/search/wst/apa?sort=date&availabilityMode=0&max_price=3000')
    s.run()
    
