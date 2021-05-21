import json
from rds.postgresql_rds import get_db
import psycopg2
import haversine
from psycopg2.extras import RealDictConnection
from haversine import haversine, Unit

from math import cos, asin, sqrt
from functools import reduce


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


def closest(data, customer):
    res = sorted(data,
                 key=lambda p: distance(customer['latitude'], customer['longitude'], p['latitude'], p['longitude']))
    return res


def latlong(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute("SELECT latitude,longitude, status from restaurant_restaurants ")
    row = curr.fetchall()
    if len(row) >= 2:
        restaurantsDataList = row
        customer = {'latitude': data['latitude'], 'longitude': data['longitude']}
        result = closest(restaurantsDataList, customer)
        response = result[:10]

        rs = []
        for items in response:
            restaurants_lat_long = (items['latitude'], items['longitude'])  # (lat, lon)
            customers_lat_logn = (data['latitude'], data['longitude'])

            distance_li = haversine(restaurants_lat_long, customers_lat_logn)

            if distance_li <= 5:
                # if items.get('status') == "Open":
                rs.append(items['latitude'])

        find_lat = tuple(rs)
        return find_lat
    else:
        return []


def get_restaurants(event):
    lat_long = latlong(event)
    conn = get_db()
    curr = conn.cursor()
    if len(lat_long) >= 2:
        curr.execute(
            "SELECT id, restaurant_name, restaurant_email, restaurant_phone, restaurant_about,restaurant_address_line_1,restaurant_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_profile_picture AS restaurant_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_thumbnail AS restaurant_thumbnail,country,zip_code,city,state, latitude,longitude, restaurant_old_new_status, type_of_restaurant,food_prepare_avg_time,special_foods,food_price_icon, status, restaurant_active, restaurants_rating, total_customer_review, pickup_delivery_status, free_delivery, offer  from restaurant_restaurants where latitude IN {} ORDER BY id ASC ".format(
                lat_long))
        row = curr.fetchall()
        return row

    elif len(lat_long) >= 1:
        curr.execute(
            "SELECT id, restaurant_name, restaurant_email, restaurant_phone, restaurant_about,restaurant_address_line_1,restaurant_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_profile_picture AS restaurant_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_thumbnail AS restaurant_thumbnail,country,zip_code,city,state, latitude,longitude, restaurant_old_new_status, type_of_restaurant,food_prepare_avg_time,special_foods,food_price_icon, status, restaurant_active, restaurants_rating, total_customer_review, pickup_delivery_status, free_delivery, offer  from restaurant_restaurants where latitude = {} ".format(
                lat_long[0]))
        row = curr.fetchall()
        return row
    else:
        return []


def lambda_handler(event, context):
    restaurant_details = get_restaurants(event)

    return {
        "body": restaurant_details
    }
