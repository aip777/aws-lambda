import json
from rds.postgresql_rds import get_db


def get_food_menu():
    conn = get_db()
    curr = conn.cursor()
    # curr.execute("SELECT food_id, food_name, food_uom,food_active, food_price, food_details, food_discounts, food_ads, restaurant_id, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| food_picture AS food_picture  from food_items")

    # curr.execute("SELECT variant_name, food_name from food_items INNER JOIN food_variants ON (food_variants.variant_name = food_items.food_name)")
    # curr.execute("SELECT food_food.id, food_food_restaurant.restaurants_id, food_food.food_name, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| food_picture AS food_picture, food_food.food_active, food_variant.id, food_variant.food_title, food_variant.food_uom,food_variant.food_details, food_variant.food_price, food_variant.food_discounts, food_variant.variant_active, food_variant.food_id, food_variant.type_of_food from food_food INNER JOIN food_variant ON food_food.id = food_variant.food_id INNER JOIN food_food_restaurant ON food_food.id = food_food_restaurant.food_id  ")
    # curr.execute("SELECT food_food.id, food_food.restaurant_id, food_food.food_name, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| food_picture AS food_picture, food_food.food_active, food_variant.id, food_variant.food_title, food_variant.food_uom,food_variant.food_details, food_variant.food_price, food_variant.food_discounts, food_variant.variant_active, food_variant.food_id, food_variant.type_of_food from food_food INNER JOIN food_variant ON food_food.id = food_variant.food_id ")

    curr.execute(
        "SELECT food_foodmenu.id, food_foodmenu_food_variants.variant_id, food_foodmenu.food_menu_name, food_foodmenu.food_menu_details,food_foodmenu.food_menu_price, food_foodmenu.food_menu_discounts, food_foodmenu.menu_active, food_foodmenu.type_of_food_menu, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| food_menu_image AS food_menu_image from food_foodmenu INNER JOIN food_foodmenu_food_variants ON food_foodmenu.id = food_foodmenu_food_variants.foodmenu_id ")

    row = curr.fetchall()
    return row


def lambda_handler(event, context):
    foods = get_food_menu()
    return {
        'statusCode': 'success',
        "body": foods
    }