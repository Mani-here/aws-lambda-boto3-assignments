import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = 'vol-0b518d57ed1ed4412'
RETENTION_DAYS = 30

def lambda_handler(event, context):

    deleted_snapshots = []

    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=f'Automated backup snapshot for {VOLUME_ID}'
    )

    snapshot_id = snapshot['SnapshotId']

    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {
                'Key': 'CreatedBy',
                'Value': 'Lambda'
            },
            {
                'Key': 'BackupType',
                'Value': 'Automated'
            }
        ]
    )

    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'tag:CreatedBy',
                'Values': ['Lambda']
            },
            {
                'Name': 'tag:BackupType',
                'Values': ['Automated']
            }
        ]
    )

    for snap in snapshots['Snapshots']:
        start_time = snap['StartTime']

        if start_time < cutoff:
            ec2.delete_snapshot(
                SnapshotId=snap['SnapshotId']
            )
            deleted_snapshots.append(
                snap['SnapshotId']
            )

    return {
        'created_snapshot': snapshot_id,
        'deleted_snapshots': deleted_snapshots
    }