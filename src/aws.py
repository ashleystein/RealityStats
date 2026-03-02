import boto3
import json
from botocore.exceptions import ClientError


def get_secret(secret_name, user='reality_stats_user', region_name="us-east-1", ):
    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name=user)
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise Exception

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Parse the JSON string into a dictionary
    return json.loads(secret)