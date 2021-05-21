import json
from rds.postgresql_rds import get_db
import psycopg2
import haversine
from psycopg2.extras import RealDictConnection

from math import cos, asin, sqrt
from functools import reduce
from haversine import haversine, Unit


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
    curr.execute("SELECT latitude, longitude from coffeehouse_coffeehouse ")
    row = curr.fetchall()

    if len(row) >= 2:

        coffeesDataList = row
        customer = {'latitude': data['latitude'], 'longitude': data['longitude']}
        result = closest(coffeesDataList, customer)
        response = result[:10]

        rs = []
        for items in response:
            coffee_house_lat_long = (items['latitude'], items['longitude'])  # (lat, lon)
            customers_lat_logn = (data['latitude'], data['longitude'])

            distance_li = haversine(coffee_house_lat_long, customers_lat_logn)
            if distance_li <= 5:
                # if items.get('status') == "Open":
                rs.append(items['latitude'])

        find_lat = tuple(rs)
        return find_lat
    else:
        return []


def get_coffee_house(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    lat_long = latlong(event)
    conn = get_db()
    curr = conn.cursor()
    if len(lat_long) >= 2:
        curr.execute(
            "SELECT id, coffee_house_name, coffee_house_email, coffee_house_phone, coffee_house_about,coffee_house_address_line_1,coffee_house_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_profile_picture AS coffee_house_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_thumbnail AS coffee_house_thumbnail,coffee_house_country,coffee_house_zip_code,coffee_house_city, coffee_house_state,latitude,longitude, coffee_house_old_new_status, type_of_coffee,coffee_prepare_avg_time,special_coffee,coffee_house_price_icon, coffee_house_status, coffee_house_active, coffee_house_rating, total_customer_review, coffee_house_offer  from coffeehouse_coffeehouse where latitude IN {} ORDER BY id ASC".format(
                lat_long))
        coffee_house_list = curr.fetchall()
        return coffee_house_list
    elif len(lat_long) >= 1:
        curr.execute(
            "SELECT id, coffee_house_name, coffee_house_email, coffee_house_phone, coffee_house_about,coffee_house_address_line_1,coffee_house_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_profile_picture AS coffee_house_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_thumbnail AS coffee_house_thumbnail,coffee_house_country,coffee_house_zip_code,coffee_house_city, coffee_house_state,latitude,longitude, coffee_house_old_new_status, type_of_coffee,coffee_prepare_avg_time,special_coffee,coffee_house_price_icon, coffee_house_status, coffee_house_active, coffee_house_rating, total_customer_review, coffee_house_offer  from coffeehouse_coffeehouse where latitude = {} ".format(
                lat_long[0]))
        coffee_house_list = curr.fetchall()
        return coffee_house_list
    else:
        return []


def lambda_handler(event, context):
    coffee_house_details = get_coffee_house(event)
    return {
        "body": coffee_house_details
    }
