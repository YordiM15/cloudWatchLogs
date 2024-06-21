import boto3
from botocore.exceptions import ClientError

def set_log_group_retention(log_group_name, retention_days):
    client = boto3.client('logs')
    try:
        client.put_retention_policy(
            logGroupName=log_group_name,
            retentionInDays=retention_days
        )
        print(f'Successfully set retention policy for log group: {log_group_name} to {retention_days} days')
    except ClientError as e:
        print(f'Error setting retention policy for log group: {log_group_name}')
        print(e)

def main():
    client = boto3.client('logs')
    retention_days = 30  # Set your desired retention period in days here

    paginator = client.get_paginator('describe_log_groups')
    for page in paginator.paginate():
        log_groups = page['logGroups']
        for log_group in log_groups:
            log_group_name = log_group['logGroupName']
            retention = log_group.get('retentionInDays')
            
            # Skip specific log groups and those with a retention period already set
            if log_group_name == "/aws/lambda/aws-controltower-NotificationForwarder" or "AWSReservedSSO" in log_group_name:
                print(f'Skipping log group: {log_group_name}')
                continue

            # Only modify log groups with "Never Expire"
            if retention is None:
                print(f'Setting retention policy for log group: {log_group_name}')
                set_log_group_retention(log_group_name, retention_days)
                print(f'Retention policy set to {retention_days} days for log group: {log_group_name}')
            else:
                print(f'Skipping log group: {log_group_name} (Retention: {retention} days)')

if __name__ == "__main__":
    main()

