import json

import psycopg2
from psycopg2.extras import RealDictConnection

from math import cos, asin, sqrt
from functools import reduce
from haversine import haversine, Unit

def get_db():
    conn = psycopg2.connect(dbname="", user="", password="", host="", connection_factory=RealDictConnection)
    return conn


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


def closest(data, customer):
    res = sorted(data,
                 key=lambda p: distance(customer['latitude'], customer['longitude'], p['latitude'], p['longitude']))
    print(res)
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
            lyon = (items['latitude'], items['longitude'])  # (lat, lon)
            paris = (data['latitude'], data['longitude'])
            distance_li = haversine(lyon, paris)
            print("DDDDDDDDDDDDDDDDDDD", distance_li)
            if distance_li<5:
                if items.get('status') == "Open":
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
            "SELECT id, restaurant_name, restaurant_email, restaurant_phone, restaurant_about,restaurant_address_line_1,restaurant_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_profile_picture AS restaurant_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_thumbnail AS restaurant_thumbnail,country,zip_code,city,state, latitude,longitude, restaurant_old_new_status, type_of_restaurant,food_prepare_avg_time,special_foods,food_price_icon, status, restaurant_active, restaurants_rating, total_customer_review, pickup_delivery_status, free_delivery, offer  from restaurant_restaurants where latitude = {} ORDER BY id ASC ".format(
                lat_long[0]))
        row = curr.fetchall()
        return row
    else:
        return []


def lambda_handler(event):
    restaurant_details = get_restaurants(event)

    return {
        "body": restaurant_details
    }


data = {
  "latitude": 23.883437464927344,
  "longitude": 90.3957399878918
}

data_error = {
  "latitude": 23.834025576182437,
  "longitude": 90.43600212558202
}

data_near = {
  "latitude": 23.7864303457115,
  "longitude": 90.41088174370515
}


result = lambda_handler(data)
print(json.dumps(result))