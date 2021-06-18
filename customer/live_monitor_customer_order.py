import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db


def get_order_history(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    try:
        conn = get_db()
        curr = conn.cursor()

        if data.get('customer_id'):
            curr.execute(
                "SELECT id, order_id, order_amount, order_status, payment_status, delivery_address, postcode, city, waiter_tips, order_type, to_char(delivery_time, 'MON-DD-YYYY HH12:MIPM') AS delivery_time, to_char(date_time, 'MON-DD-YYYY HH12:MIPM') AS date_time, customer_id, coffee_house_id, restaurant_id from order_order  where customer_id = {} ORDER BY id DESC ".format(
                    data['customer_id']))
            obj = curr.fetchall()
            return obj
        else:
            return []

    except Exception as e:
        return e


def lambda_handler(event, context):
    data = json.loads(event['body']) if event.get('body', 0) else event

    response = get_order_history(event)
    return {
        'body': response
    }