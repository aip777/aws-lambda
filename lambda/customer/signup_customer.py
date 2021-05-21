import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import psycopg2
from psycopg2.extras import RealDictConnection
import hashlib
from rds.postgresql_rds import get_db

USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''


def insert_data(event):
    conn = get_db()
    data = json.loads(event['body']) if event.get('body', 0) else event
    password = data['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    curr = conn.cursor()
    curr.execute("SELECT username from customer_customer where email= '{}'".format(data['email']))
    row = curr.fetchone()

    if data['email'] != row:

        cur = conn.cursor()
        cur.execute(
            "insert into customer_customer(first_name ,last_name, date_of_birth, address_line_1, address_line_2, mobile, city, state ,country ,zip_code ,signup_location, signup_ip, email, password, username, geolocation_long, geolocation_lat) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (data['first_name'],
             data['last_name'],
             data['date_of_birth'],
             data['address_line_1'],
             data['address_line_2'],
             data['mobile'],
             data['city'],
             data['state'],
             data['country'],
             data['zip_code'],
             data['signup_location'],
             data['signup_ip'],
             data['email'],
             password_hash,
             data['username'],
             data['geolocation_long'],
             data['geolocation_lat']
             ))
        conn.commit()
        cur.close()
    else:
        return 'This email address already exists'


def get_data(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute("SELECT username from customer_customer where email= '{}'".format(data['email']))
    row = curr.fetchone()
    # datai = []
    # while row is not None:
    #     row = curr.fetchone()
    #     datai.append(row)
    return row


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def lambda_handler(event, context):
    for field in ["username", "email", "password", "first_name"]:
        if not event.get(field):
            return {"error": False, "success": True, 'message': f"{field} is not present", "data": None}

    username = event['username']
    email = event["email"]
    password = event['password']
    name = event["first_name"]
    client = boto3.client('cognito-idp')
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': "name",
                    'Value': name
                },
                {
                    'Name': "email",
                    'Value': email
                }
            ],
            ValidationData=[
                {
                    'Name': "email",
                    'Value': email
                },
                {
                    'Name': "custom:username",
                    'Value': username
                }
            ])

    except client.exceptions.UsernameExistsException as e:
        return {
            "status": "error",
            #   "error": False,
            #   "success": True,
            "message": "This username already exists",
            #   "data": None
        }
    except client.exceptions.InvalidPasswordException as e:

        return {
            "status": "error",
            # "error": False,
            # "success": True,
            "message": "Password should have Caps,Special chars, Numbers",
            #   "data": None
        }
    except client.exceptions.UserLambdaValidationException as e:
        return {
            "status": "error",
            #   "error": False,
            #   "success": True,
            "message": "Email already exists",
            #   "data": None
        }

    except Exception as e:
        return {
            "status": "error",
            # "error": False,
            # "success": True,
            "message": str(e),
            #   "data": None
        }
    insert_data(event)
    datai = get_data(event)
    return {
        "status": "success",
        # "error": False,
        # "success": True,
        # "message": "Please confirm your signup, check Email for validation code",
        "message": "Check Email for validation code",
        # "data": None,
        "body": datai
    }
