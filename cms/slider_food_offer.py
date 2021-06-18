import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db
import datetime

import haversine
from haversine import haversine, Unit

from math import cos, asin, sqrt
from functools import reduce


# --------------------------------------------------start restaurant---------------------------------------------------------------

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


# ------------------------------------------------- end restaurants------------------------------------------------------

# ------------------------------------------------- start coffee house------------------------------------------------------

def latlong_coffee_house(event):
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
    lat_long = latlong_coffee_house(event)
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

    # ---------------------------------------------------------- end coffee house-----------------------------------------------------


def food_offer(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute("SELECT id, end_date_time, start_date_time from cms_restaurantsslider")
    obj = curr.fetchall()
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    current_time = str(datetime.datetime.now())

    slider_list = []

    for date_time_from_db in obj:
        end_time_db = str(date_time_from_db['end_date_time'])
        end_times = end_time_db[:-6] + '.0'
        time_diff = datetime.datetime.strptime(end_times, datetimeFormat) - datetime.datetime.strptime(current_time,
                                                                                                       datetimeFormat)
        diff = time_diff.days
        if diff >= 0:
            curr = conn.cursor()
            curr.execute(
                "SELECT cms_restaurantsslider.id, food_food.food_name, food_food.food_price, cms_restaurantsslider.discount_price, cms_restaurantsslider.after_discount_price ,'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| cms_restaurantsslider.slider_image AS slider_image, cms_restaurantsslider.food_id, cms_restaurantsslider.restaurant_id, cms_restaurantsslider.slider_offer from cms_restaurantsslider INNER JOIN food_food ON cms_restaurantsslider.food_id = food_food.id  where cms_restaurantsslider.id= {}  ".format(
                    date_time_from_db['id']))
            slider_list.append(curr.fetchone())
            #   from food_food INNER JOIN food_variant ON food_food.id = food_variant.food_id where food_food.restaurant_id= {}".format(data['restaurant_id']))
        else:
            print("Slider not found")
    return slider_list


def coffee_offer(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute("SELECT id, end_date_time, start_date_time from cms_coffeeoffer")
    obj = curr.fetchall()
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    current_time = str(datetime.datetime.now())

    coffee_offer_list = []

    for date_time_from_db in obj:
        end_time_db = str(date_time_from_db['end_date_time'])
        end_times = end_time_db[:-6] + '.0'
        time_diff = datetime.datetime.strptime(end_times, datetimeFormat) - datetime.datetime.strptime(current_time,
                                                                                                       datetimeFormat)
        diff = time_diff.days
        if diff >= 0:
            curr = conn.cursor()
            curr.execute(
                "SELECT cms_coffeeoffer.id, coffeehouse_coffee.coffee_name, coffeehouse_coffee.coffee_price, cms_coffeeoffer.discount_price,  cms_coffeeoffer.coffee_offer, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| cms_coffeeoffer.slider_image AS slider_image, cms_coffeeoffer.coffee_id, cms_coffeeoffer.coffee_house_id, cms_coffeeoffer.after_discount_price  from cms_coffeeoffer  INNER JOIN coffeehouse_coffee ON cms_coffeeoffer.coffee_id = coffeehouse_coffee.id  where cms_coffeeoffer.id= {}  ".format(
                    date_time_from_db['id']))
            coffee_offer_list.append(curr.fetchone())
            #   from food_food INNER JOIN food_variant ON food_food.id = food_variant.food_id where food_food.restaurant_id= {}".format(data['restaurant_id']))
        else:
            print("Slider not found")
    return coffee_offer_list


def lambda_handler(event, context):
    food_offer_list = food_offer(event)
    coffee_offer_list = coffee_offer(event)

    restaurant_details = get_restaurants(event)

    food_offer_slider = []
    for obj in restaurant_details:
        restaurant_id = obj['id']

        for food_offer_info in food_offer_list:
            slier_restaurant_id = food_offer_info['restaurant_id']

            if restaurant_id == slier_restaurant_id:
                food_offer_slider.append(food_offer_info)
                # res = get_restaurants_rating(event)

    coffee_house = get_coffee_house(event)
    coffee_offer_slider = []
    for obj in coffee_house:
        coffee_house_id = obj['id']

        for coffee_offer_info in coffee_offer_list:
            slier_coffee_house_id = coffee_offer_info['coffee_house_id']

            if coffee_house_id == slier_coffee_house_id:
                coffee_offer_slider.append(coffee_offer_info)

    return {
        "body": {
            "food_offer_slider": food_offer_slider,
            "coffee_offer_slider": coffee_offer_slider
        }
    }
