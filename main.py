import time
from slackclient import SlackClient
import os


def get_permalink(client: SlackClient, channel: str, ts: str):
    res = client.api_call(
        'chat.getPermalink',
        channel=channel,
        message_ts=ts
    )
    print(res)
    return res['permalink']


def get_content(client: SlackClient, channel: str, ts: str):
    res = client.api_call(
        'channels.history',
        channel=channel,
        oldest=ts,
        latest=ts,
        inclusive=True
    )
    print(res)
    return res['messages'][0]['text']


def check_reaction(events, stamp):
    for event in events:
        if 'type' in event and event['type'] == 'reaction_added' and event['reaction'] == stamp:
            print(event)
            return event
    return None


sc = SlackClient(os.environ['SLACK_API_TOKEN'])
if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        event = check_reaction(events, 'kaggle_grandmaster')
        if event is not None:
            item = event['item']
            message = get_content(sc, item['channel'], item['ts'])
            link = get_permalink(sc, item['channel'], item['ts'])
            sc.rtm_send_message(event['item']['channel'],
                                f'スタンプが押されたよ！\ntext: {message}\nlink: {link}')
        time.sleep(1)
