import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db


def get_order_history(event):
    data = json.loads(event['body']) if event.get('body', 0) else event

    try:
        conn = get_db()
        curr = conn.cursor()

        if data.get('customer_id'):
            # curr.execute("SELECT order_order.total_amount, order_order.ordered_by_id, order_order.status, order_order.order_type, order_orderitem.quantity, order_orderitem.food_item_id, order_orderitem.order_id, order_orderitem.restaurant_id, order_orderitem.food_note from order_orderitem INNER JOIN order_order on order_orderitem.order_id =  order_order.id  where order_orderitem.restaurant_id= {} ORDER BY order_orderitem.order_id ASC ".format(data['restaurant_id']))
            curr.execute(
                "SELECT id, order_id, order_amount, order_status, payment_status, payment_id, delivery_address, postcode, city, waiter_tips, order_type, to_char(delivery_time, 'MON-DD-YYYY HH12:MIPM') AS delivery_time, to_char(date_time, 'MON-DD-YYYY HH12:MIPM') AS date_time, customer_id, coffee_house_id, restaurant_id from order_order  where customer_id= {} ORDER BY id ASC ".format(
                    data['customer_id']))
            obj = curr.fetchall()
            print("DDDD", obj)

            object_info = []
            food_id = []
            for object in obj:
                customer_id = object['customer_id']
                restaurant_id = object['restaurant_id']
                coffee_house_id = object['coffee_house_id']
                order_id = object['id']

                curr.execute(
                    "SELECT id, first_name, last_name, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| customer_profile_pic AS customer_profile_pic, email, address_line_1, address_line_2, mobile from customer_customer  where id = {} ".format(
                        customer_id))
                customer_info = curr.fetchone()
                object["customer"] = customer_info

                if restaurant_id:
                    curr.execute(
                        "SELECT id, restaurant_name, restaurant_phone, restaurant_about, restaurant_address_line_1, restaurant_address_line_2, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_profile_picture AS restaurant_profile_picture, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| restaurant_thumbnail AS restaurant_thumbnail, country, zip_code, city, state, restaurant_linkedin, restaurant_website, restaurant_facebook, restaurant_instagram, restaurant_twitter, latitude, longitude, restaurant_old_new_status, type_of_restaurant, food_prepare_avg_time, special_foods, food_price_icon, restaurants_rating, total_customer_review, pickup_delivery_status, free_delivery, offer, status, restaurant_active, restaurant_email from restaurant_restaurants  where id = {} ".format(
                            restaurant_id))
                    restaurant_info = curr.fetchone()
                    object["restaurant"] = restaurant_info

                    curr.execute(
                        "SELECT id, food_quantity, variant_quantity, food_note, food_id, food_variant_id, order_id, item_total from order_restaurantorder  where order_id = {} ".format(
                            order_id))
                    food_item_info = curr.fetchall()
                    object["food_items"] = food_item_info

                    addon_list = []

                    food_list = []
                    food_variant_list = []
                    addon_details = []
                    for food_items in food_item_info:
                        food_id = food_items['food_id']
                        food_variant_id = food_items['food_variant_id']
                        food_items_id = food_items['id']

                        if food_id:
                            curr.execute(
                                "SELECT id, food_name, food_picture, food_price, discount_type, discount_price, after_discount_price, food_stock, food_availability, food_active, type_of_food, food_components, food_review, food_offer, food_details, category_id restaurant_id from food_food  where id = {} ".format(
                                    food_id))
                            food_info = curr.fetchone()
                            food_list.append(food_info)
                        else:
                            curr.execute(
                                "SELECT id, variant_title, variant_price, food_id from food_variant  where id = {} ".format(
                                    food_variant_id))
                            food_info = curr.fetchone()
                            food_variant_list.append(food_info)

                    curr.execute(
                        "SELECT id, addon_quantity, item_total, food_addon_id, order_id from order_restaurantorderaddon  where order_id = {} ".format(
                            order_id))
                    addon_order_details = curr.fetchall()
                    #  addon_list.append(addon_info)

                    for addon_list in addon_order_details:
                        addon = addon_list['food_addon_id']
                        curr.execute(
                            "SELECT id, addon_name, price, food_name_id from food_foodaddons  where id = {} ".format(
                                addon))
                        addon_details_info = curr.fetchone()
                        addon_details.append(addon_details_info)

                    object['food'] = food_list
                    object['food_variant'] = food_variant_list
                    object['addon'] = addon_details

                    object_info.append(object)

                # coffee order history

                if coffee_house_id:
                    curr.execute(
                        "SELECT id, coffee_house_name, coffee_house_email, coffee_house_phone, coffee_house_about, coffee_house_address_line_1, coffee_house_address_line_2, coffee_house_profile_picture, coffee_house_thumbnail, coffee_house_linkedin, coffee_house_website, coffee_house_facebook, coffee_house_instagram, coffee_house_twitter, coffee_house_country, coffee_house_zip_code, coffee_house_city, coffee_house_state, latitude, longitude, coffee_house_old_new_status, type_of_coffee, coffee_prepare_avg_time, special_coffee, coffee_house_price_icon, coffee_house_rating, total_customer_review, coffee_house_offer, coffee_house_status, coffee_house_active from coffeehouse_coffeehouse  where id = {} ".format(
                            coffee_house_id))
                    coffee_house_info = curr.fetchone()
                    object["coffee_house"] = coffee_house_info

                    curr.execute(
                        "SELECT id, coffee_quantity, coffee_id, order_id, item_total, coffee_note from order_coffeeorder  where order_id = {} ".format(
                            order_id))
                    coffee_item_info = curr.fetchall()
                    object["coffee_items"] = coffee_item_info

                    coffee_list = []
                    addon_details = []
                    for coffee_items in coffee_item_info:
                        coffee_id = coffee_items['coffee_id']

                        if coffee_id:
                            curr.execute(
                                "SELECT id, coffee_name, coffee_availability, coffee_price, type_of_coffee, coffee_review, coffee_components, quantity, coffee_picture, coffee_offer, coffee_details, coffee_active, coffee_house_id, after_discount_price, discount_price, discount_type from coffeehouse_coffee where id = {} ".format(
                                    coffee_id))
                            coffee_info = curr.fetchone()
                            coffee_list.append(coffee_info)

                    curr.execute(
                        "SELECT id, addon_quantity, item_total, coffee_addons_id, order_id from order_coffeeaddonorder  where order_id = {} ".format(
                            order_id))
                    addon_order_details = curr.fetchall()
                    #  addon_list.append(addon_info)

                    for addon_list in addon_order_details:
                        addon = addon_list['coffee_addons_id']
                        curr.execute(
                            "SELECT id, coffee_addon_name, coffee_addon_price, coffee_id from coffeehouse_coffeeaddons  where id = {} ".format(
                                addon))
                        addon_details_info = curr.fetchone()
                        addon_details.append(addon_details_info)

                    object['coffee'] = coffee_list
                    object['addon'] = addon_details

                    object_info.append(object)
            return object_info

    except Exception as e:
        return e


def lambda_handler(event, context):
    data = json.loads(event['body']) if event.get('body', 0) else event

    response = get_order_history(event)
    return {
        'body': response
    }