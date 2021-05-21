import json
from rds.postgresql_rds import get_db
import psycopg2
from psycopg2.extras import RealDictConnection


def table_qr(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute(
        "SELECT table_name,number_of_seat,about_table,id, restaurant_id, coffee_house_id from waiter_diningtable where qr_code= '{}'".format(
            data['qr_code']))
    obj = curr.fetchall()

    if obj:
        for property_list in obj:

            restaurant_id = property_list['restaurant_id']
            coffee_house_id = property_list['coffee_house_id']

            if restaurant_id:
                curr.execute(
                    "SELECT restaurant_restaurants.restaurant_name, restaurant_restaurants.restaurant_phone, restaurant_restaurants.restaurant_about, restaurant_restaurants.restaurant_address_line_1, restaurant_restaurants.restaurant_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_restaurants.restaurant_profile_picture AS restaurant_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_restaurants.restaurant_thumbnail AS restaurant_thumbnail , restaurant_restaurants.country, restaurant_restaurants.zip_code,restaurant_restaurants.city, restaurant_restaurants.state, restaurant_restaurants.latitude, restaurant_restaurants.longitude, restaurant_restaurants.restaurant_old_new_status, restaurant_restaurants.type_of_restaurant, restaurant_restaurants.food_prepare_avg_time, restaurant_restaurants.special_foods, restaurant_restaurants.food_price_icon, restaurant_restaurants.restaurants_rating, restaurant_restaurants.total_customer_review, restaurant_restaurants.pickup_delivery_status, restaurant_restaurants.free_delivery, restaurant_restaurants.offer, restaurant_restaurants.status, restaurant_restaurants.restaurant_active, restaurant_restaurants.restaurant_email, waiter_diningtable.id, waiter_diningtable.table_name, waiter_diningtable.number_of_seat, waiter_diningtable.about_table, waiter_diningtable.coffee_house_id, waiter_diningtable.qr_code, waiter_diningtable.table_icon, waiter_diningtable.table_status, waiter_diningtable.is_active, waiter_diningtable.restaurant_id from waiter_diningtable INNER JOIN restaurant_restaurants ON waiter_diningtable.restaurant_id = restaurant_restaurants.id  where waiter_diningtable.restaurant_id = {} ".format(
                        restaurant_id))
                obj = curr.fetchone()

                return obj
            elif coffee_house_id:
                curr.execute(
                    "SELECT coffeehouse_coffeehouse.coffee_house_name, coffeehouse_coffeehouse.coffee_house_email,coffeehouse_coffeehouse.coffee_house_phone, coffeehouse_coffeehouse.coffee_house_about, coffeehouse_coffeehouse.coffee_house_address_line_1, coffeehouse_coffeehouse.coffee_house_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffeehouse_coffeehouse.coffee_house_profile_picture AS coffee_house_profile_picture,'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffeehouse_coffeehouse.coffee_house_thumbnail AS coffee_house_thumbnail, coffeehouse_coffeehouse.coffee_house_website, coffeehouse_coffeehouse.coffee_house_country, coffeehouse_coffeehouse.coffee_house_zip_code, coffeehouse_coffeehouse.coffee_house_city, coffeehouse_coffeehouse.coffee_house_state, coffeehouse_coffeehouse.latitude, coffeehouse_coffeehouse.longitude,coffeehouse_coffeehouse.coffee_house_old_new_status, coffeehouse_coffeehouse.type_of_coffee, coffeehouse_coffeehouse.coffee_prepare_avg_time, coffeehouse_coffeehouse.special_coffee, coffeehouse_coffeehouse.coffee_house_price_icon, coffeehouse_coffeehouse.coffee_house_rating, coffeehouse_coffeehouse.total_customer_review, coffeehouse_coffeehouse.coffee_house_offer, coffeehouse_coffeehouse.coffee_house_status, coffeehouse_coffeehouse.coffee_house_active, waiter_diningtable.id, waiter_diningtable.table_name, waiter_diningtable.number_of_seat, waiter_diningtable.about_table, waiter_diningtable.qr_code, waiter_diningtable.table_icon, waiter_diningtable.table_status, waiter_diningtable.is_active, waiter_diningtable.coffee_house_id, waiter_diningtable.restaurant_id from waiter_diningtable INNER JOIN coffeehouse_coffeehouse ON waiter_diningtable.coffee_house_id = coffeehouse_coffeehouse.id where waiter_diningtable.coffee_house_id= {} ".format(
                        coffee_house_id))
                obj = curr.fetchone()

                return obj
    else:
        return []


def table_info(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    if event.get("restaurant_id"):
        curr.execute(
            "SELECT restaurant_restaurants.restaurant_name, restaurant_restaurants.restaurant_phone, restaurant_restaurants.restaurant_about, restaurant_restaurants.restaurant_address_line_1, restaurant_restaurants.restaurant_address_line_2, restaurant_restaurants.restaurant_profile_picture, restaurant_restaurants.restaurant_thumbnail, restaurant_restaurants.country, restaurant_restaurants.zip_code,restaurant_restaurants.city, restaurant_restaurants.state, restaurant_restaurants.latitude, restaurant_restaurants.longitude, restaurant_restaurants.restaurant_old_new_status, restaurant_restaurants.type_of_restaurant, restaurant_restaurants.food_prepare_avg_time, restaurant_restaurants.special_foods, restaurant_restaurants.food_price_icon, restaurant_restaurants.restaurants_rating, restaurant_restaurants.total_customer_review, restaurant_restaurants.pickup_delivery_status, restaurant_restaurants.free_delivery, restaurant_restaurants.offer, restaurant_restaurants.status, restaurant_restaurants.restaurant_active, restaurant_restaurants.restaurant_email, waiter_diningtable.id, waiter_diningtable.table_name, waiter_diningtable.number_of_seat, waiter_diningtable.about_table, waiter_diningtable.qr_code, waiter_diningtable.table_icon, waiter_diningtable.table_status, waiter_diningtable.is_active, waiter_diningtable.restaurant_id from waiter_diningtable INNER JOIN restaurant_restaurants ON waiter_diningtable.restaurant_id = restaurant_restaurants.id  where waiter_diningtable.restaurant_id = {} ".format(
                data['restaurant_id']))
        obj = curr.fetchall()
        return obj
    elif event.get("coffee_house_id"):
        curr.execute(
            "SELECT coffeehouse_coffeehouse.coffee_house_name, coffeehouse_coffeehouse.coffee_house_email,coffeehouse_coffeehouse.coffee_house_phone, coffeehouse_coffeehouse.coffee_house_about, coffeehouse_coffeehouse.coffee_house_address_line_1, coffeehouse_coffeehouse.coffee_house_address_line_2,coffeehouse_coffeehouse.coffee_house_profile_picture, coffeehouse_coffeehouse.coffee_house_thumbnail, coffeehouse_coffeehouse.coffee_house_website, coffeehouse_coffeehouse.coffee_house_country, coffeehouse_coffeehouse.coffee_house_zip_code, coffeehouse_coffeehouse.coffee_house_city, coffeehouse_coffeehouse.coffee_house_state, coffeehouse_coffeehouse.latitude, coffeehouse_coffeehouse.longitude,coffeehouse_coffeehouse.coffee_house_old_new_status, coffeehouse_coffeehouse.type_of_coffee, coffeehouse_coffeehouse.coffee_prepare_avg_time, coffeehouse_coffeehouse.special_coffee, coffeehouse_coffeehouse.coffee_house_price_icon, coffeehouse_coffeehouse.coffee_house_rating, coffeehouse_coffeehouse.total_customer_review, coffeehouse_coffeehouse.coffee_house_offer, coffeehouse_coffeehouse.coffee_house_status, coffeehouse_coffeehouse.coffee_house_active, waiter_diningtable.id, waiter_diningtable.table_name, waiter_diningtable.number_of_seat, waiter_diningtable.about_table, waiter_diningtable.qr_code, waiter_diningtable.table_icon, waiter_diningtable.table_status, waiter_diningtable.is_active, waiter_diningtable.coffee_house_id from waiter_diningtable INNER JOIN coffeehouse_coffeehouse ON waiter_diningtable.coffee_house_id = coffeehouse_coffeehouse.id where waiter_diningtable.coffee_house_id= {} ".format(
                data['coffee_house_id']))
        obj = curr.fetchall()
        return obj


def lambda_handler(event, context):
    if event.get("qr_code"):
        response = table_qr(event)
    elif event.get("restaurant_id") or event.get("coffee_house_id"):
        response = table_info(event)
    return {
        'body': response
    }
