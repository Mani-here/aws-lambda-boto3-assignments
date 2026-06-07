import boto3

ec2 = boto3.client("ec2")

def lambda_handler(event, context):
    stopped = []
    started = []

    auto_stop = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Action", "Values": ["Auto-Stop"]},
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    for reservation in auto_stop["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            ec2.stop_instances(InstanceIds=[instance_id])
            stopped.append(instance_id)

    auto_start = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Action", "Values": ["Auto-Start"]},
            {"Name": "instance-state-name", "Values": ["stopped"]}
        ]
    )

    for reservation in auto_start["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            ec2.start_instances(InstanceIds=[instance_id])
            started.append(instance_id)

    return {
        "stopped_instances": stopped,
        "started_instances": started
    }