import json
import time

from issue_chan.issue import IssueManager
from issue_chan.slack import SlackManager
from issue_chan.utils import get_logger, load_mapping, update_mapping

MAPPING_PATH = 'config/mapping.json'


def check_reaction(event):
    """issueスタンプがついていたらissueを立て、slackにURLを通知する"""

    event = slack.check_reaction(event, 'issue')
    if event is not None:
        channel, ts = event['item']['channel'], event['item']['ts']

        # 紐付いているリポジトリがなければ使い方を表示
        if channel not in mapping:
            send_usage(channel)
            return

        content = slack.get_content(channel, ts)
        link = slack.get_permalink(channel, ts)

        issue_body = f"{content}\nlink: {link}"
        iss, created = issue.create(mapping[channel], content, issue_body)

        if created:
            message = f"issueを作成しました！\n" \
                f"→ {iss.html_url}"
        else:
            message = f"同じissueが既にありますよ！\n" \
                f"→ {iss.html_url}"
        slack.send_message(channel, message)


def check_command(event):
    """設定項目が発言されたら設定し、そうでなければ使い方を提示"""

    prefixes = ('issue-chan', 'issue_chan')
    if 'type' in event and 'text' in event and event['type'] == 'message':
        texts = event['text'].split()
        if texts[0] not in prefixes:
            return

        channel = event['channel']
        if len(texts) >= 3 and texts[1] == 'set':
            # リポジトリのマッピングを変更
            repo = texts[2]
            mapping[channel] = repo
            update_mapping(MAPPING_PATH, mapping)
            message = f"このチャンネルと `{repo}` を紐付けました！"
            slack.send_message(channel, message)
            logger.info('link channel=%s -> repository=%s', channel, repo)
        else:
            send_usage(channel)


def send_usage(channel):
    message = open("usage.txt").read().format(app_public_url=config['app_public_url'])
    slack.send_message(channel, message)


def main():
    slack.client.rtm_connect()
    logger.info('connect RTM api')
    while slack.client.server.connected:
        events = slack.client.rtm_read()
        for event in events:
            logger.debug(event)
            check_command(event)
            check_reaction(event)
        time.sleep(1)


if __name__ == '__main__':
    logger = get_logger('issue_chan')
    with open('config/config.json') as f:
        config = json.load(f)
        logger.info('load config.json')

    slack = SlackManager(config['slack_api_token'])
    issue = IssueManager(config['github_hostname'], config['app_id'], config['app_installation_id'])
    mapping = load_mapping(MAPPING_PATH)
    main()
