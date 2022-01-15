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

def send_to_slack():
    # ID of the channel you want to send the message to
    channel_id = os.environ.get("SLACK_CHANNEL_ID")

    try:
        # Call the chat.postMessage method using the WebClient
        result = web_client.chat_postMessage(
            channel=channel_id,
            text="Hello world"
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")

def lambda_handler(event, context):
    get_aws_cost()
    send_to_slack()
