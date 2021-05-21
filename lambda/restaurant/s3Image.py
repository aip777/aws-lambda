import boto3
import json
import psycopg2
import base64
from psycopg2.extras import RealDictConnection

s3 = boto3.resource('s3')


def get_db():
    conn = psycopg2.connect(dbname="", user="", password="",
                            host="",
                            connection_factory=RealDictConnection)
    return conn


def insert_data(image_name, event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    s3_bucket_url = 'https://mapplate-public.s3.eu-central-1.amazonaws.com/' + image_name
    conn = get_db()
    conn.autocommit = True
    cur = conn.cursor()
    sql = """ UPDATE customers
                SET  profile_img_url = %s
                WHERE customer_id = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(sql,
                    (s3_bucket_url,
                     data['customer_id']))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


def timezone(event):
    conn = get_db()
    curr = conn.cursor()
    curr.execute("SET timezone TO 'Asia/Dhaka';")
    curr.execute("SELECT now();")
    row = curr.fetchall()
    return row


def get_data(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute(
        "SELECT  'https://s3.console.aws.amazon.com/s3/buckets/mapplate-public/media/path/'|| profile_img_url AS profile_img_url  from customers where customer_id= '{}'".format(
            data['customer_id']))
    row = dict(curr.fetchone())

    return row['profile_img_url']


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    data = json.loads(event['body']) if event.get('body', 0) else event
    # name = data['customer_profile_pic']
    # customer_id = data['customer_id']
    # image_id = str(id(customer_id))
    # image_name = str(image_id +'_customer_id_{}.png'.format(customer_id))

    # insert_data(image_name, event)
    # decode_content = base64.b64decode(name)
    # s3.put_object(Bucket='mapplate-public', Key=image_name, Body=decode_content)
    # url = get_data(event)
    row = timezone(event)
    return {
        "status": "success",
        # "profile_img_url": url,
        "test": "{}".format(row)
    }