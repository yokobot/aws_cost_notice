# coding; utf-8
import boto3
from slack_sdk.web import WebClient

def get_aws_cost():
    ce = boto3.client('ce')
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
    client = WebClient()
    response = client.api_test()
    print(response)

def lambda_handler(event, context):
    get_aws_cost()
    send_to_slack()
