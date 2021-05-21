import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db


def lambda_handler(event, context):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    cur = conn.cursor()
    if data.get('restaurant_id'):
        cur.execute(
            "SELECT id, restaurant_name, restaurant_email, restaurant_phone, restaurant_about, restaurant_address_line_1, restaurant_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_profile_picture AS restaurant_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_thumbnail AS restaurant_thumbnail, restaurant_linkedin, restaurant_website, restaurant_facebook, restaurant_instagram, restaurant_twitter, country, zip_code, city, state, restaurant_active, user_id, latitude, longitude, status, type_of_restaurant, food_prepare_avg_time, food_price_icon, special_foods, restaurant_old_new_status, restaurants_rating, pickup_delivery_status, total_customer_review, free_delivery, offer from restaurant_restaurants where id={}".format(
                data['restaurant_id']))
        info = cur.fetchall()

        return {
            'body': info
        }

    elif data.get('coffee_house_id'):
        cur.execute(
            "SELECT id, coffee_house_name, coffee_house_email, coffee_house_phone, coffee_house_about, coffee_house_address_line_1, coffee_house_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_profile_picture AS coffee_house_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_thumbnail AS coffee_house_thumbnail, coffee_house_linkedin, coffee_house_website, coffee_house_facebook, coffee_house_instagram, coffee_house_twitter, coffee_house_country, coffee_house_zip_code, coffee_house_city, coffee_house_state, latitude, longitude, coffee_house_old_new_status, type_of_coffee, coffee_prepare_avg_time, special_coffee, coffee_house_price_icon, coffee_house_rating, total_customer_review, coffee_house_offer, coffee_house_status, coffee_house_active, user_id from coffeehouse_coffeehouse where id={}".format(
                data['coffee_house_id']))
        info = cur.fetchall()

        return {
            'body': info
        }
