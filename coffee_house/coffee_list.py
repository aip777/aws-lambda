import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db


def get_coffee_list(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()

    coffee_object = []

    curr = conn.cursor()
    curr.execute(
        "SELECT  id, coffee_name, coffee_availability, coffee_price, discount_type, discount_price, after_discount_price, type_of_coffee, coffee_review, coffee_components, quantity,'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_picture AS coffee_picture, coffee_offer, coffee_details, coffee_active from coffeehouse_coffee where coffee_house_id= {}".format(
            data['coffee_house_id']))
    coffee_list = curr.fetchall()

    if coffee_list:
        for coffee_item in coffee_list:
            coffee_availability = int(coffee_item['coffee_availability'])

            if coffee_list and coffee_availability == 1:
                # for coffee in coffee_list:
                # Get coffee id
                coffee_id = coffee_item['id']
                # get food addon list
                curr.execute(
                    "SELECT id, coffee_addon_name, coffee_addon_price from coffeehouse_coffeeaddons where coffee_id = {}".format(
                        coffee_id))
                coffee_addon_item = curr.fetchall()
                coffee_item['coffee_addon'] = coffee_addon_item

                # append coffee item
                coffee_object.append(coffee_item)
        return coffee_object


def lambda_handler(event, context):
    coffee = get_coffee_list(event)

    if not coffee:
        return {"body": []}

    return {
        "body": coffee
    }

