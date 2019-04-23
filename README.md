# issue-chan

<img src="https://avatars.slack-edge.com/2019-04-19/613268541333_b3d98b8479b877664c89_512.jpg" width=100>

↑issueを作るという強い意志を感じる

GitHub上で特定のemojiでreactionしたら、そのメッセージをissueとして立てる

要件：

- realtime messaging apiからreactionを取得
- reactionされたitemのchannelとtsを取得
- 投稿のpermalinkとcontentを取得
- GitHubにissueを立てる

## 使い方

### config/config.jsonを作る

config.sample.jsonをコピーして作ると良いです。

```json
{
  "slack_api_token": "YOUR_SLACK_API_TOKEN",
  "github_app_id": "YOUR_APP_ID",
  "github_installation_id": "YOUR_INSTALLATION_ID",
  "github_hostname": "github.com"
}
```


### デプロイ

このフォルダを丸ごとコピーして以下をタイプ。python3.7以降とpipenvが必要です。

`$ pipenv run python main.py`

### GitHubで行う設定

Repositoryにissue-chanを設定します。

### Slackで行う設定

使いたいチャンネルにissue-chanをinviteします。

## アイコン

https://enjoynet.co.jp/free_snsicon/menherachan_3/
にて配布されている素材を使っています。