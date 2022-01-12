# coding; utf-8
import boto3

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

def lambda_handler(event, context):
    get_aws_cost()
