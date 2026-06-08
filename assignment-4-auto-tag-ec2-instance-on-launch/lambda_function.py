import boto3
from datetime import datetime, timezone

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    instance_id = event['detail']['instance-id']

    launch_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                'Key': 'LaunchDate',
                'Value': launch_date
            },
            {
                'Key': 'CreatedBy',
                'Value': 'Lambda-AutoTag'
            },
            {
                'Key': 'Environment',
                'Value': 'Assignment'
            }
        ]
    )

    return {
        'message': 'Tags added successfully',
        'instance_id': instance_id,
        'launch_date': launch_date
    }