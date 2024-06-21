import boto3
import argparse
from botocore.exceptions import ClientError
import logging

# Habilitar logging para boto3
boto3.set_stream_logger(name='botocore')

def get_log_groups_with_retention(retention_days, region_name):
    client = boto3.client('logs', region_name=region_name)
    paginator = client.get_paginator('describe_log_groups')
    
    matching_log_groups = []

    for page in paginator.paginate():
        log_groups = page.get('logGroups', [])
        for log_group in log_groups:
            if log_group.get('retentionInDays') == retention_days:
                matching_log_groups.append(log_group['logGroupName'])

    return matching_log_groups

def main():
    parser = argparse.ArgumentParser(description="Encuentra grupos de logs de CloudWatch con un período de retención específico.")
    parser.add_argument('--region', type=str, default='us-east-1', help='Región de AWS a usar')
    args = parser.parse_args()

    retention_days = 90  # 3 months

    try:
        matching_log_groups = get_log_groups_with_retention(retention_days, args.region)

        if matching_log_groups:
            print(f'Grupos de logs con un período de retención de {retention_days} días:')
            for log_group in matching_log_groups:
                print(log_group)
        else:
            print(f'No se encontraron grupos de logs con un período de retención de {retention_days} días.')
    except ClientError as e:
        logging.error('ClientError en main:')
        logging.error(e)
    except Exception as e:
        logging.error('Error inesperado en main:')
        logging.error(e)

if __name__ == "__main__":
    main()

