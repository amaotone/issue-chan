import json
import time

from issue_chan.issue import IssueManager
from issue_chan.slack import SlackManager
from issue_chan.utils import get_logger


def check_reaction(event):
    """issueスタンプがついていたらissueを立て、slackにURLを通知する"""
    event = slack.check_reaction(event, 'issue')
    if event is not None:
        channel, ts = event['item']['channel'], event['item']['ts']
        content = slack.get_content(channel, ts)
        link = slack.get_permalink(channel, ts)

        issue_body = f"{content}\nlink: {link}"
        iss, created = issue.create('amane-suzuki/sandbox', content, issue_body)

        if created:
            slack_message = f"issueを作成しました！\n{iss.html_url}"
        else:
            slack_message = f"同じissueが既にありますよ！\n{iss.html_url}"
        slack.send_message(channel, slack_message)


def check_reply(event):
    """replyで設定項目が飛んできたら設定し、そうでなければusageを提示"""
    pass


def main():
    slack.client.rtm_connect()
    logger.info('connect RTM api')
    while slack.client.server.connected:
        events = slack.client.rtm_read()
        for event in events:
            check_reply(event)
            check_reaction(event)
        time.sleep(1)


if __name__ == '__main__':
    logger = get_logger('issue_chan')
    with open('config.json') as f:
        config = json.load(f)
        logger.info('load config.json')

    slack = SlackManager(config['slack_api_token'])
    issue = IssueManager(config['github_hostname'], config['github_app_id'], config['github_installation_id'])
    main()
