from datetime import datetime, timedelta
from typing import Optional, Tuple

import jwt
import requests
from github import Github
from github.Issue import Issue

from .utils import get_logger


class IssueManager(object):
    def __init__(self, hostname, app_id, installation_id):
        if hostname is None or hostname in ['github.com', 'api.github.com']:
            base_url = 'https://api.github.com'
        else:
            base_url = f'https://{hostname}/api/v3'

        token = _get_auth_token(hostname, app_id, installation_id)
        self.client = Github(base_url=base_url, login_or_token=token)
        self.logger = get_logger(__name__)

    def create(self, repo_name, title, body, **kwargs) -> Tuple[Issue, bool]:
        """issueを作る"""
        repo = self.client.get_repo(repo_name)
        issue = self.search_issue_by_title(repo_name, title)

        # すでに同名のissueがあったら、新しくつくることはしない
        if issue is not None:
            self.logger.info('issue already exists: repo=%s, title=%s', repo_name, title)
            return issue, False

        repo.create_issue(title=title, body=body, **kwargs)
        issue = self.search_issue_by_title(repo_name, title)
        self.logger.info('issue created: repo=%s, title=%s, number=%s', repo_name, issue.title, issue.number)
        return issue, True

    def search_issue_by_title(self, repo_name, title) -> Optional[Issue]:
        repo = self.client.get_repo(repo_name)
        issues = repo.get_issues(state='open')
        for issue in issues:
            if issue.title == title:
                return issue
        return None


def _get_private_pem():
    path = 'issue-chan.pem'
    with open(path, 'r', encoding='utf-8') as f:
        key = f.readlines()
        key = ''.join(key)
    return key


def _get_auth_token(hostname, app_id, installation_id):
    utcnow = datetime.utcnow() + timedelta(seconds=-5)
    duration = timedelta(seconds=30)
    payload = {
        'iat': utcnow,
        'exp': utcnow + duration,
        'iss': app_id
    }
    pem = _get_private_pem()
    encoded = jwt.encode(payload, pem, 'RS256')
    headers = {
        'Authorization': f"Bearer {encoded.decode('utf-8')}",
        'Accept': 'application/vnd.github.machine-man-preview+json'
    }
    if hostname == 'github.com':
        base_url = 'api.github.com'
    else:
        base_url = f'{hostname}/api/v3'
    url = f'https://{base_url}/app/installations/{installation_id}/access_tokens'
    resp = requests.post(url, headers=headers)
    if not resp.ok:
        print(resp.json()['message'])
        resp.raise_for_status()
    token = resp.json()['token']
    return token
