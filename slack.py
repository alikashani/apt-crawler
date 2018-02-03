from slackclient import SlackClient


class SlackConn(object):

    def __init__(self, slack_token):
        self.conn = SlackClient(slack_token)

    def send_message(self, message, mrkdwn=True):
        self.conn.api_call(
          "chat.postMessage",
          channel="#apartments",
          user="apartment hunter",
          mrkdwn= mrkdwn,
          text=message
        )

    def send_new_listing(self, listing):
        message = """
Title: *{name}*
Price: {price}
Area: {area}
Link: {url}""".format(name=listing['name'], price=listing['price'], area=listing['area'], url=listing['url'])
        self.send_message(message)

    def send_update_listing(self, listing):
        message = """
Title: *{name}*
Price: {price} CHANGE IN PRICE BY ${update}
Area: {area}
Link: {url}""".format(name=listing['name'], price=listing['price'], update=listing['update'], area=listing['area'], url=listing['url'])
        self.send_message(message)