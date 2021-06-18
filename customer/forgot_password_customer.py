import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid

import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db

from cognito.aws_cognito_auth import cognito_aws

cognito_access = cognito_aws()
USER_POOL_ID = cognito_access[0]
CLIENT_ID = cognito_access[2]
CLIENT_SECRET = cognito_access[1]


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(
        str(CLIENT_SECRET).encode('utf-8'),
        msg=str(msg).encode('utf-8'),
        digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    data = json.loads(event['body']) if event.get('body', 0) else event
    # elif(re.search(regex,data['username'])):

    if data['username']:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT email FROM customer_customer WHERE email LIKE '{}'".format(data['username']))
        row = cur.fetchone()
        cur.close()

        if row is None:
            return {
                "status": "success",
                "message": "Email is not valid"
            }
        try:
            username = event['username']
            response = client.forgot_password(
                ClientId=CLIENT_ID,
                SecretHash=get_secret_hash(username),
                Username=username,

            )

        except client.exceptions.UserNotFoundException:
            return {"status": "error",
                    "message": "Username doesnt exists"}

        except client.exceptions.InvalidParameterException:
            return {"status": "error",
                    "message": f"User <{username}> is not confirmed yet"}

        except client.exceptions.CodeMismatchException:
            return {"status": "error",
                    "message": "Invalid Verification code"}

        except client.exceptions.NotAuthorizedException:
            return {"status": "error",
                    "message": "User is already confirmed"}

        except client.exceptions.LimitExceededException:
            return {"status": "error",
                    "message": "Limit Exceeded Exception"}

        except Exception as e:
            return {"status": "error",
                    "message": f"Uknown    error {e.__str__()} "}

        return {
            "status": "success",
            "message": f"Please check your Registered email id for validation code"
        }

    else:
        return {
            "status": "error"
        }