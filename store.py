from tinydb import TinyDB, Query


class Store(object):

    def __init__(self, db_name):
        self.db = TinyDB(db_name)
        self.table =  self.db.table('listings')

    def get(self, id):
        listing = Query()
        return self.table.get(listing.id == id)

    def get_dupes(self, name, geotag):
        listing = Query()
        dupes = []
        resps = self.table.search(listing.name == name)
        for resp in resps:
            if resp['geotag'] == geotag:
                dupes.append(resp)
        return dupes

    def price_difference(self, old_price, new_price):
        if self.real_price(old_price) > self.real_price(new_price):
            return self.real_price(old_price) - self.real_price(new_price)
        return 0

    def min_price_diff(self, new_listing, old_listings):
        price_diffs = []
        for ol in old_listings:
            price_diffs.append(self.price_difference(ol['price'], new_listing['price']))
        return min(price_diffs)

    def real_price(self, string_price):
        return int(string_price[1:])

    def insert(self, listing):
        self.table.insert(listing)

    def update(self, listing):
        query = Query()
        self.table.upsert(listing, query.id == listing['id'])

    def all(self):
        return self.table.all()