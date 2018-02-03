from slackclient import SlackClient


class SlackConn(object):

    def __init__(self, slack_token):
        self.conn = SlackClient(slack_token)

    def send_message(self, message, channel="#listings", mrkdwn=True):
        self.conn.api_call(
          "chat.postMessage",
          channel=channel,
          mrkdwn= mrkdwn,
          text=message
        )

    def send_new_listing(self, listing):
        message = """
Title: *{name}*
Link: {url}
Price: {price}
Area: {area}""".format(name=listing['name'], price=listing['price'], area=listing['area'], url=listing['url'])
        self.send_message(message)

    def send_update_listing(self, listing):
        message = """
Title: *{name}*
Link: {url}
Price: {price} *CHANGE IN PRICE BY ${update}*
Area: {area}""".format(name=listing['name'], price=listing['price'], update=listing['update'], area=listing['area'], url=listing['url'])
        self.send_message(message, "#priceupdates")
