from craigslist import CraigslistHousing
from datetime import datetime, timedelta
from store import Store
from slack import SlackConn
import os


db = Store("listings.json")
slack = SlackConn(os.environ["SLACK_TOKEN"])

from_time = datetime.now() - timedelta(hours=1)
cl_h = CraigslistHousing(site='losangeles', filters={'max_price': 3000})
boxes = [[(-118.488483356,33.8709965384),
          (-118.3696936831,34.0313337674)]]

# Lots of lazy code, but really need to use my own crawler for speed...
for listing in cl_h.get_results(sort_by='newest', geotagged=True):
    dt = datetime.strptime(listing["datetime"], "%Y-%m-%d %H:%M")
    if from_time > dt:
        break
    if 'geotag' not in listing:
        continue
    try:
        lat, lng = listing['geotag']
        passed = True
        for box in boxes:
            if lat < box[0][1] or lat > box[1][1] or lng < box[0][0] or lng > box[1][0]:
                passed = False
        if not passed:
            continue
    except:
        continue

    old_listing = db.get(listing['id'])
    if old_listing:
        print("old listing found")
        price_diff = db.price_difference(old_listing['price'], listing['price'])
        if price_diff > 0:
            listing['update'] = str(price_diff)
            print("price diff", price_diff)
            db.update(listing)
            slack.send_update_listing(listing)
        continue

    old_listings = db.get_dupes(listing['name'], listing['geotag'])
    if old_listings:
        print("dupe listings found")
        price_diff = db.min_price_diff(listing, old_listings)
        if price_diff > 0:
            listing['update'] = str(price_diff)
            print("price diff", price_diff)
            db.update(listing)
            slack.send_update_listing(listing)
        continue

    # normal
    print("normal")
    db.insert(listing)
    slack.send_new_listing(listing)

