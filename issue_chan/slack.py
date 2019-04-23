from slackclient import SlackClient
from .utils import get_logger

class SlackManager(object):
    def __init__(self, slack_api_token):
        self.client = SlackClient(slack_api_token)
        self.logger = get_logger(__name__)

    def get_permalink(self, channel: str, ts: str):
        res = self.client.api_call(
            'chat.getPermalink',
            channel=channel,
            message_ts=ts
        )
        self.logger.info("get permalink: %s", res['permalink'])
        return res['permalink']


    def get_content(self, channel: str, ts: str):
        res = self.client.api_call(
            'channels.history',
            channel=channel,
            oldest=ts,
            latest=ts,
            inclusive=True
        )
        self.logger.info("message found: %s", res['messages'][0])
        return res['messages'][0]['text']

    def check_reaction(self, event, stamp):
        if 'type' in event and event['type'] == 'reaction_added' and event['reaction'] == stamp:
            self.logger.info("reaction found: channel=%s, ts=%s", event['item']['channel'], event['item']['ts'])
            return event
        return None

    def send_message(self, channel:str, message: str):
        self.logger.info("send message: channel=%s", channel)
        self.client.rtm_send_message(channel, message)