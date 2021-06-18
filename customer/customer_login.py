import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db

USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def initiate_auth(client, username, password):
    secret_hash = get_secret_hash(username)
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password,
            })
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None


def get_data(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute(
        "SELECT id,username,first_name,last_name, date_of_birth, address_line_1,address_line_2,mobile,city,state,country,zip_code, notification_token, signup_ip,geolocation_long,geolocation_lat, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| customer_profile_pic AS customer_profile_pic from customer_customer where email= '{}'".format(
            data['username']))
    row = curr.fetchone()
    # datai = []
    # while row is not None:
    #     row = curr.fetchone()
    #     datai.append(row)
    return row


def update_vendor(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE customer_customer
                SET first_name = %s, last_name = %s, date_of_birth = %s, address_line_1 = %s, address_line_2 = %s, mobile = %s, city = %s, state = %s, country = %s, zip_code = %s, signup_ip = %s, geoLocation_long = %s, geoLocation_lat = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = get_db()
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql,
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
                     data['signup_ip'],
                     data['geoLocation_long'],
                     data['geoLocation_lat'],
                     data['id']))
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


def update_user_geolocation(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE customer_customer
                SET  notification_token = %s, signup_ip = %s, geoLocation_long = %s, geoLocation_lat = %s
                WHERE username = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(sql,
                    (data['notification_token'],
                     data['signup_ip'],
                     data['geoLocation_long'],
                     data['geoLocation_lat'],
                     data['username']))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


def insert_profile_data(event):
    s3 = boto3.client("s3")
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    conn.autocommit = True
    cur = conn.cursor()
    sql = """ UPDATE customer_customer 
                SET  customer_profile_pic = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        name = data['customer_profile_pic']
        customer_id = data['id']
        image_id = str(id(customer_id))
        image_name = str(image_id + '_customer_id_{}.png'.format(customer_id))
        decode_content = base64.b64decode(name)
        s3.put_object(Bucket='mapplate-public', Key='media/customer_profile_pic/' + image_name, ContentType="image/png",
                      Body=decode_content)
        # s3_bucket_url = 'https://mapplate-public.s3.eu-central-1.amazonaws.com/' + image_name
        s3_bucket_url = 'customer_profile_pic/' + image_name

        conn = get_db()
        cur = conn.cursor()
        cur.execute(sql,
                    (s3_bucket_url,
                     data['id']))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    data = json.loads(event['body']) if event.get('body', 0) else event
    for field in ["username", "password"]:
        if event.get(field) is None:
            return {
                "status": "error",
                "message": f"{field} is required"
            }

    username = data['username']
    password = data['password']
    resp, msg = initiate_auth(client, username, password)

    insert_profile_data(event)
    update_user_geolocation(event)
    update_vendor(event)
    datai = get_data(event)

    if msg != None:
        return {
            "status": "error",
            "message": "The email or password is incorrect"
        }

    if resp.get("AuthenticationResult"):
        return {
            "status": "success",
            "body": datai,
            "data": {
                #   "id_token": resp["AuthenticationResult"]["IdToken"],
                #   "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                "access_token": resp["AuthenticationResult"]["AccessToken"]
                #   "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                #   "token_type": resp["AuthenticationResult"]["TokenType"]
            }}
    else:  # this code block is relevant only when MFA is enabled
        return {
            "status": "error"
        }
