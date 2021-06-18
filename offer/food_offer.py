import json
from rds.postgresql_rds import get_db
import psycopg2
from psycopg2.extras import RealDictConnection

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
    curr.execute("SELECT latitude,longitude from restaurant_restaurants ")
    row = curr.fetchall()

    restaurantsDataList = row
    customer = {'latitude': data['latitude'], 'longitude': data['longitude']}
    result = closest(restaurantsDataList, customer)
    response = result[:10]

    rs = []
    for items in response:
        rs.append(items['latitude'])

    find_lat = tuple(rs)
    return find_lat


def closest_coffee_house(data, customer):
    res = sorted(data,
                 key=lambda p: distance(customer['latitude'], customer['longitude'], p['latitude'], p['longitude']))
    return res


def coffee_house_latlong(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute("SELECT latitude,longitude from coffeehouse_coffeehouse ")
    row = curr.fetchall()

    coffee_house = row
    customer = {'latitude': data['latitude'], 'longitude': data['longitude']}
    result = closest_coffee_house(coffee_house, customer)
    response = result[:10]

    rs = []
    for items in response:
        rs.append(items['latitude'])

    find_lat = tuple(rs)
    return find_lat


def get_food_offer(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    lat_long = latlong(event)
    coffee_house_lat_long = coffee_house_latlong(event)
    conn = get_db()
    curr = conn.cursor()

    if latlong:
        curr.execute(
            "SELECT id, restaurant_name, restaurant_email, restaurant_phone, restaurant_about, restaurant_address_line_1, restaurant_address_line_2,'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_profile_picture AS restaurant_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_thumbnail AS restaurant_thumbnail, country, zip_code, city, state, restaurant_linkedin, restaurant_website, restaurant_facebook, restaurant_instagram, restaurant_twitter, latitude, longitude, restaurant_old_new_status, type_of_restaurant, food_prepare_avg_time, special_foods, food_price_icon, restaurants_rating, total_customer_review, pickup_delivery_status, free_delivery, offer, status, restaurant_active from restaurant_restaurants where latitude IN {} ORDER BY id ASC".format(
                lat_long))
        restaurants_id = curr.fetchall()

        offer_list = []

        for rest in restaurants_id:
            curr = conn.cursor()
            curr.execute(
                "SELECT  id, food_name, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| food_picture AS food_picture, food_price, discount_type, discount_price, after_discount_price, food_stock, food_availability, food_active, type_of_food, food_components, food_review, food_offer, food_details, category_id, food_time_id, restaurant_id from food_food where restaurant_id= {} ORDER BY id ASC".format(
                    rest['id']))
            food_item = curr.fetchall()

            variant_list = []
            food_addon_list = []
            food_list_obj = []
            for food in food_item:
                food_id = food['id']

                discount_price = food['discount_price']
                if discount_price:
                    curr.execute(
                        "SELECT id, addon_name, price from food_foodaddons where food_name_id = {}".format(food_id))
                    food_addon_item = curr.fetchall()
                    food["addon"] = food_addon_item

                    curr.execute(
                        "SELECT id, variant_title, variant_price, food_id from food_variant where food_id = {}".format(
                            food_id))
                    variant_item = curr.fetchall()
                    food['variant_list'] = variant_item

                    food_list_obj.append(food)
            rest["food"] = food_list_obj
            offer_list.append(rest)

        return offer_list
    else:
        return "Restaurant latitude and longitude not found"


def get_coffee_offer(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    lat_long = latlong(event)
    coffee_house_lat_long = coffee_house_latlong(event)
    conn = get_db()
    curr = conn.cursor()

    if coffee_house_lat_long:

        curr.execute(
            "SELECT id, coffee_house_name, coffee_house_email, coffee_house_phone, coffee_house_about, coffee_house_address_line_1, coffee_house_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_profile_picture AS coffee_house_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_house_thumbnail AS coffee_house_thumbnail, coffee_house_linkedin, coffee_house_website, coffee_house_facebook, coffee_house_instagram, coffee_house_twitter, coffee_house_country, coffee_house_zip_code, coffee_house_city, coffee_house_state, latitude, longitude, coffee_house_old_new_status, type_of_coffee, coffee_prepare_avg_time, special_coffee, coffee_house_price_icon, coffee_house_rating, total_customer_review, coffee_house_offer, coffee_house_status, coffee_house_active from coffeehouse_coffeehouse where latitude IN {} ORDER BY id ASC".format(
                coffee_house_lat_long))
        coffee_house_list = curr.fetchall()
        coffee_list = []
        for rest in coffee_house_list:
            curr = conn.cursor()
            curr.execute(
                "SELECT id, coffee_name, coffee_availability, coffee_price, type_of_coffee, coffee_review, coffee_components, quantity, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| coffee_picture AS coffee_picture, coffee_offer, coffee_details, coffee_active, coffee_house_id, after_discount_price, discount_price, discount_type from coffeehouse_coffee where coffee_house_id= {} ORDER BY id ASC".format(
                    rest['id']))
            coffee_item = curr.fetchall()

            coffee_list_obj = []
            for coffee in coffee_item:
                coffee_id = coffee['id']

                discount_price = coffee['discount_price']
                if discount_price:
                    curr.execute(
                        "SELECT id, coffee_addon_name, coffee_addon_price, coffee_id from coffeehouse_coffeeaddons where coffee_id = {}".format(
                            coffee_id))
                    variant_item = curr.fetchall()
                    coffee['addons'] = variant_item
                    coffee_list_obj.append(coffee)

            rest["coffee"] = coffee_list_obj
            coffee_list.append(rest)

        return coffee_list
    else:
        return "Coffee house latitude and longitude not found"


def lambda_handler(event, context):
    # TODO implement
    food = get_food_offer(event)
    coffee = get_coffee_offer(event)

    context = {
        "coffee": coffee,
        "restaurant": food
    }

    food_offer = []
    coffe_offer = []
    for item in context.values():
        for obj in item:
            if obj.get('food'):
                food_offer.append(obj)
            if obj.get('coffee'):
                coffe_offer.append(obj)
    return {
        "body": {
            "coffee": coffe_offer,
            "restaurant": food_offer
        }
    }