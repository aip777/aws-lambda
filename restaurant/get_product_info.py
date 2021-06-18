import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db


def lambda_handler(event, context):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    if data.get('food_id'):
        curr.execute(
            "SELECT id, food_name,'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| food_picture AS food_picture, food_price, discount_type, discount_price, after_discount_price, food_stock, food_availability, food_active, type_of_food, food_components, food_review, food_offer, food_details, category_id, food_time_id, restaurant_id  from food_food where id = {}".format(
                data['food_id']))
        product = curr.fetchall()

        return {
            'body': product
        }

    elif data.get('coffee_id'):
        curr.execute(
            "SELECT id, coffee_name, coffee_availability, coffee_price, type_of_coffee, coffee_review, coffee_components, quantity, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_picture AS coffee_picture, coffee_offer, coffee_details, coffee_active, coffee_house_id, after_discount_price, discount_price, discount_type from coffeehouse_coffee where id={}".format(
                data['coffee_id']))
        product = curr.fetchall()

        return {
            'body': product
        }
