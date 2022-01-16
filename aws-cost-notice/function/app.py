# coding; utf-8
import logging
import os
import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logger = logging.getLogger(__name__)


web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
ce = boto3.client('ce')


def get_aws_cost():
    #TODO 引数で日付を取れるようにする
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': '2022-01-10',
            'End': '2022-01-11'
        },
        Granularity='DAILY',
        Metrics=[
            'BlendedCost',
        ]
    )
    print(response)
    # TODO blended costで良いかを確認する
    daily_cost = response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
    return(str(daily_cost))


def send_to_slack(daily_cost):
    # ID of the channel you want to send the message to
    channel_id = os.environ.get("SLACK_CHANNEL_ID")

    try:
        # Call the chat.postMessage method using the WebClient
        result = web_client.chat_postMessage(
            channel=channel_id,
            text="昨日の AWS 料金は %s ドルです" % daily_cost
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


def lambda_handler(event, context):
    daily_cost = get_aws_cost()
    send_to_slack(daily_cost)
