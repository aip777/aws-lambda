import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db

import mollie
import requests
from mollie.api.client import Client


def payment_handler(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE order_order
                SET payment_status = %s
                WHERE id = %s"""
    conn = None
    if data['payment_status'] == 'PENDING':
        updated_rows = 0
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(sql,
                        (data['payment_status'], data['order_id']))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows
    elif data['payment_status'] == 'PAID':
        mollie_client = Client()
        mollie_client.set_api_key('')

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT payment_id from order_order where id={}".format(data['order_id']))
        row = cur.fetchone()
        payment_id = row['payment_id']
        payment = mollie_client.payments.get(payment_id)
        if payment.is_paid():
            updated_rows = 0
            try:
                conn = get_db()
                cur = conn.cursor()
                cur.execute(sql,
                            (data['payment_status'], data['order_id']))
                updated_rows = cur.rowcount
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            return updated_rows
        else:
            updated_rows = 0
            payment_status = 'PENDING'
            try:
                conn = get_db()
                cur = conn.cursor()
                cur.execute(sql,
                            (payment_status, data['order_id']))
                updated_rows = cur.rowcount
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            return updated_rows


def order(event):
    data = json.loads(event['body']) if event.get('body', 0) else event

    mollie_client = Client()
    mollie_client.set_api_key('')

    price = "{:.2f}".format(data['total_amount'])
    payment = mollie_client.payments.create({
        'amount': {
            'currency': 'USD',
            'value': price
        },
        'description': 'Mapplate',
        'redirectUrl': 'https://www.mapplate.com/success/',
        'webhookUrl': 'https://www.mapplate.com/',
    })
    payment_id = payment['id']

    conn = get_db()
    conn.autocommit = True
    cur = conn.cursor()

    if data.get('food_list'):
        cur.execute("SELECT user_id from restaurant_restaurants where id={}".format(data['restaurant_id']))
        row = cur.fetchone()
        restaurant_owner_id = row['user_id']
        payment_status = "PENDING"

        status = data['FromStatus']

        if status == "DeliveryStatus":
            order_type = "DELIVERY"
        elif status == "PickupStatus":
            order_type = "PICKUP"
        elif status == "Dining":
            order_type = "DINING"
        else:
            order_type = "Not Found"

        cur = conn.cursor()
        # conn.autocommit = True
        cur.execute(
            "insert into order_order(order_id, order_amount, order_status, payment_status, payment_id, delivery_address, postcode, city, waiter_tips, order_type, delivery_time, date_time, customer_id, coffee_house_id, restaurant_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
            (data['total_amount'], data['delivery_address'], data['status'], data['customer_id'], payment_id,
             restaurant_owner_id, data['waitertip'], payment_status, order_type, data['Datetime'], data['Delivarytime'],
             data['restaurant_id']))
        order_id_list = cur.fetchone()
        order_id = order_id_list['id']

        object_list = data.get('food_list')
        for food_items in object_list:
            cur.execute(
                "insert into order_restaurantorder(order_id, food_item_id, quantity,food_note,restaurant_id) values(%s,%s,%s,%s,%s) RETURNING id;",
                (order_id,
                 food_items['id'],
                 food_items['CountItem'],
                 food_items['FoodNote'],
                 food_items['restaurant_id']
                 ))
            food_item_id = cur.fetchone()
            food_item = food_item_id['id']

            food_addons = food_items['foodaddons']
            if food_addons:
                for addon in food_addons:
                    cur.execute(
                        "insert into order_restaurantorder_foodaddon(restaurantorder_id,foodaddons_id) values(%s,%s)",
                        (food_item,
                         addon['id']
                         ))

        conn.commit()
        conn.close()

    elif data.get('coffee_list'):
        cur.execute("SELECT user_id from coffeehouse_coffeehouse where id={}".format(data['coffee_house_id']))
        row = cur.fetchone()
        coffee_owner_id = row['user_id']
        payment_status = "PENDING"

        if data['FromStatus'] == "DeliveryStatus":
            order_type = "DELIVERY"
        elif data['FromStatus'] == "PickupStatus":
            order_type = "PICKUP"
        elif data['FromStatus'] == "Dining":
            order_type = "DINING"

        cur = conn.cursor()
        # conn.autocommit = True
        cur.execute(
            "insert into order_order(total_amount, delivery_address, status, ordered_by_id, payment_id, user_id, waiter_tips,payment_status,order_type,date_time,delivery_time, coffee_house_id ) values(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
            (data['total_amount'], data['delivery_address'], data['status'], data['customer_id'], payment_id,
             coffee_owner_id, data['waitertip'], payment_status, order_type, data['Datetime'], data['Delivarytime'],
             data['coffee_house_id']))
        order_id_list = cur.fetchone()
        order_id = order_id_list['id']

        object_list = data.get('coffee_list')
        for coffee_items in object_list:
            cur.execute(
                "insert into order_coffeeorder(coffee_order_id, coffee_id, coffee_quantity, coffee_note, coffee_house_id) values(%s,%s,%s,%s,%s) RETURNING id;",
                (order_id,
                 coffee_items['id'],
                 coffee_items['CountItem'],
                 coffee_items['FoodNote'],
                 coffee_items['coffee_house_id']
                 ))
            coffee_item_id = cur.fetchone()
            coffee_item = coffee_item_id['id']

            coffee_addons = coffee_items['coffee_addons']
            if coffee_addons:
                for addon in coffee_addons:
                    cur.execute(
                        "insert into order_coffeeorder_coffee_addons(coffeeorder_id, coffeeaddons_id) values(%s,%s)",
                        (coffee_item,
                         addon['id']
                         ))

        conn.commit()
        conn.close()

    return {
        'statusCode': 200,
        'body': {
            "order_id": order_id,
            "checkout": payment['_links']['checkout']['href']
        }
    }


def address_update(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE order_order
                SET delivery_address = %s, postcode = %s, city = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = get_db()
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql,
                    (data['update_delivery_address'],
                     data['postcode'],
                     data['city'],
                     data['order_id_num']))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


def table_status(event):
    if event.get("table"):
        sql = """ UPDATE waiter_diningtable SET  table_status = %s WHERE id = %s """
        conn = None
        updated_rows = 0
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(sql,
                        (event['table']['table_status'],
                         event['table']['table_id']))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return updated_rows


def lambda_handler(event, context):
    data = json.loads(event['body']) if event.get('body', 0) else event

    if data.get('total_amount'):
        response = order(event)
        table_status(event)
        return {
            'statusCode': "success",
            'body': response
        }

    elif data.get('order_id'):
        payment_response = payment_handler(event)
        return {
            'statusCode': "success",
            'body': payment_response
        }
    elif data.get('update_delivery_address'):
        delivery_address_update = address_update(event)
        return {
            'statusCode': "success",
            'body': delivery_address_update
        }

    else:
        return {
            'statusCode': "error"
        }

