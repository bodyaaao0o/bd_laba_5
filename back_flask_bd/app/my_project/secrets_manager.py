import boto3
import json
import os
from botocore.exceptions import ClientError


def get_secret(secret_name=None, region_name="eu-west-2"):
    """
    Отримує секрети з AWS Secrets Manager

    Args:
        secret_name: Назва секрету в AWS Secrets Manager
        region_name: AWS регіон (за замовчуванням eu-west-2)

    Returns:
        dict: Словник з секретами
    """

    # Якщо secret_name не передано, беремо з environment variable
    if not secret_name:
        secret_name = os.getenv('AWS_SECRET_NAME', 'flask-rds-credentials')

    print(f"Attempting to retrieve secret: {secret_name} from region: {region_name}")

    # Створюємо клієнт Secrets Manager
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    except Exception as e:
        print(f"Error creating AWS client: {e}")
        raise

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"Error retrieving secret: {error_code}")

        if error_code == 'ResourceNotFoundException':
            print(f"Secret '{secret_name}' not found in region {region_name}")
        elif error_code == 'InvalidRequestException':
            print(f"Invalid request for secret '{secret_name}'")
        elif error_code == 'InvalidParameterException':
            print(f"Invalid parameter for secret '{secret_name}'")
        elif error_code == 'DecryptionFailure':
            print(f"Cannot decrypt secret '{secret_name}'")
        elif error_code == 'InternalServiceError':
            print(f"AWS internal service error")

        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

    # Парсимо секрет
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        # Для бінарних секретів
        import base64
        decoded_binary_secret = base64.b64decode(
            get_secret_value_response['SecretBinary']
        )
        return json.loads(decoded_binary_secret)


def is_aws_environment():
    """
    Перевіряє чи додаток запущено в AWS середовищі
    """
    return (
            os.getenv('AWS_EXECUTION_ENV') is not None or
            os.getenv('USE_AWS_SECRETS', '').lower() == 'true' or
            os.path.exists('/opt/aws')
    )
