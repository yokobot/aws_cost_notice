# aws_cost_notice

一日前の AWS コストを slack に通知する SAM アプリケーションです。

### sam init

`sam init --runtime python3.7 --dependency-manager pip --app-template hello-world --name aws-cost-notice`

### sam build

`sam build`

### test

`sam local invoke`

### deploy

`sam deploy --guided`

### 環境変数

AWS コンソール or CLI で環境変数 `SLACK_BOT_TOKEN` と `SLACK_CHANNEL_ID` を上書いてください。
[SLACK_BOT_TOKEN](https://api.slack.com/authentication/token-types#bot)
[SLACK_CHANNEL_ID](https://api.slack.com/methods/conversations.list)