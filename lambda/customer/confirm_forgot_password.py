import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
import psycopg2
from psycopg2.extras import RealDictConnection

from botocore.exceptions import ClientError, ParamValidationError

USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''


def get_db():
    conn = psycopg2.connect(dbname="postgres", user="", password="",
                            host="m.eu-central-1.rds.amazonaws.com",
                            connection_factory=RealDictConnection)
    return conn


def update_username_password(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    if data['username'] and data['password']:
        sql = """ UPDATE customer_customer
                SET username = %s, password = %s, signup_ip = %s
                WHERE username = %s"""
        conn = None
        updated_rows = 0
        try:
            conn = get_db()
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute(sql,
                        (data['username'],
                         data['password'],
                         data['signup_ip'],
                         data['username']))
            # get the number of updated rows
            updated_rows = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    try:
        username = event['username']
        password = event['password']
        code = event['code']
        client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            ConfirmationCode=code,
            Password=password,
        )

        update_username_password(event)

    except client.exceptions.UserNotFoundException as e:
        return {
            "status": "error",
            "message": "Username doesnt exists"
        }

    except client.exceptions.InvalidPasswordException as e:
        return {
            "status": "error",
            "message": "Password should be 6 characters and contain numbers alphabet uppercase and lowercase letters"
        }

    except ParamValidationError as e:
        return {"status": "error",
                "message": "Password should be 6 characters and contain numbers alphabet uppercase and lowercase letters"}


    except client.exceptions.ExpiredCodeException as e:
        return {
            "status": "error",
            "message": "Expired Code Exception"
        }

    except client.exceptions.LimitExceededException as e:
        return {
            "status": "error",
            "message": "Try again after 15 minutes"
        }


    except client.exceptions.CodeMismatchException as e:
        return {
            "status": "error",
            "message": "Invalid Verification code"
        }

    except client.exceptions.NotAuthorizedException as e:
        return {
            "status": "error",
            "message": "User is already confirmed"}

    except Exception as e:
        return {
            "status": "error",
            "message": f"Unknown error {e.__str__()} "}

    return {
        "status": "success",
        "message": f"Password has been changed successfully",
    }
