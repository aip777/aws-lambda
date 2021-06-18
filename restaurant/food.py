import json
from rds.postgresql_rds import get_db
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictConnection
import pytz


def get_foods(event):
    conn = get_db()
    food_object = []

    curr = conn.cursor()
    curr.execute(
        "SELECT  id, food_name, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| food_picture AS food_picture, food_price, discount_type, discount_price, after_discount_price, food_stock, food_availability, food_active, type_of_food, food_components, food_review, food_offer, food_details, category_id, food_time_id, restaurant_id from food_food where restaurant_id= {}".format(
            event['restaurant_id']))
    food_item = curr.fetchall()
    if food_item:
        for food in food_item:
            # Get food id
            food_id = food['id']
            category_id = food['category_id']
            food_time = food['food_time_id']
            food_availability = int(food["food_availability"])

            # if food_availability == 1:
            # Get time
            if food_time:
                curr.execute("SELECT id, label, start, end from food_time where id = {} ".format(food_time))
                time_object = curr.fetchall()

                if time_object:

                    for time_db in time_object:
                        now = datetime.now()
                        time_m = int(now.strftime('%Y%m%d'))
                        start_time = time_db.get('start')
                        end_time = time_db.get('end')
                        mytz = pytz.timezone('Asia/Dhaka')
                        time_now = pytz.utc.localize(datetime.utcnow(), is_dst=None).astimezone(mytz).time()

                        if time_now >= start_time and time_now <= end_time:
                            # get variant list
                            curr.execute(
                                "SELECT id, variant_title, variant_price from food_variant where food_id = {}".format(
                                    food_id))
                            variant_item = curr.fetchall()
                            food['variant'] = variant_item

                            curr.execute(
                                "SELECT category_name from food_category where category_id = {}".format(category_id))
                            category = curr.fetchall()
                            for food_category in category:
                                food['category'] = food_category['category_name']

                                # get food addon list
                            curr.execute(
                                "SELECT id, addon_name, price from food_foodaddons where food_name_id = {}".format(
                                    food_id))
                            food_addon_item = curr.fetchall()
                            food['food_addon'] = food_addon_item
                            # append food item
                            food_object.append(food)
                            # else:
                        #     food_object.append([])
                else:
                    curr.execute(
                        "SELECT id, variant_title, variant_price from food_variant where food_id = {}".format(food_id))
                    variant_item = curr.fetchall()
                    food['variant'] = variant_item

                    curr.execute("SELECT category_name from food_category where category_id = {}".format(category_id))
                    category = curr.fetchall()
                    for food_category in category:
                        food['category'] = food_category['category_name']

                        # get food addon list
                    curr.execute(
                        "SELECT id, addon_name, price from food_foodaddons where food_name_id = {}".format(food_id))
                    food_addon_item = curr.fetchall()
                    food['food_addon'] = food_addon_item

                    # append food item
                    food_object.append(food)
            else:
                curr.execute(
                    "SELECT id, variant_title, variant_price from food_variant where food_id = {}".format(food_id))
                variant_item = curr.fetchall()
                food['variant'] = variant_item

                curr.execute("SELECT category_name from food_category where category_id = {}".format(category_id))
                category = curr.fetchall()
                for food_category in category:
                    food['category'] = food_category['category_name']

                # get food addon list
                curr.execute(
                    "SELECT id, addon_name, price from food_foodaddons where food_name_id = {}".format(food_id))
                food_addon_item = curr.fetchall()
                food['food_addon'] = food_addon_item

                # append food item
                food_object.append(food)

                # else:
            #     food_object.append([])
    return food_object


def lambda_handler(event, context):
    foods = get_foods(event)
    if not foods:
        return {"body": []}

    return {
        "body": foods
    }