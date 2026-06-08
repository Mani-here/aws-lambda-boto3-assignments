import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'manikandan-s3-clean-up'

def lambda_handler(event, context):

    deleted_files = []

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME
    )

    if 'Contents' not in response:
        return {
            'message': 'Bucket empty'
        }

    cutoff = datetime.now(
        timezone.utc
    ) - timedelta(days=0)

    for obj in response['Contents']:

        if obj['LastModified'] < cutoff:

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=obj['Key']
            )

            deleted_files.append(
                obj['Key']
            )

    return {
        'deleted_files': deleted_files
    }