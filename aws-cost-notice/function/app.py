# coding; utf-8
import os
import inspect
import logging
import traceback
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
ce = boto3.client('ce')


def get_aws_cost():
    """
    前日の AWS コストをドル建てで返す関数
    """
    logger.info(inspect.currentframe().f_code.co_name + ' is start.')

    today = datetime.now()
    yesterday = today - timedelta(1)

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': yesterday.strftime('%Y-%m-%d'),
                'End': today.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=[
                'UnblendedCost',
            ]
        )
        logger.info(response)
    except ClientError:
        logging.error(traceback.format_exc())

    daily_cost = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']

    logger.info(inspect.currentframe().f_code.co_name + ' is end.')
    return(str(daily_cost))


def send_to_slack(daily_cost):
    """
    slack に文字列を通知する関数
    """
    logger.info(inspect.currentframe().f_code.co_name + ' is start.')
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

    logger.info(inspect.currentframe().f_code.co_name + ' is end.')


def lambda_handler(event, context):
    """
    メイン関数
    """
    logger.info(inspect.currentframe().f_code.co_name + ' is start.')

    send_to_slack(get_aws_cost())

    logger.info(inspect.currentframe().f_code.co_name + ' is end.')
