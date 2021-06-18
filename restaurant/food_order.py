import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db
import mollie
import requests
from mollie.api.client import Client
from firebase import firebase


def user_notification(device_token):
    serverToken = 'AAAApGjplqU:APA91bHocbWGGkwWTDa1dSepTnkprIpIA89OSMcANOE2ntL5tuwG2iFbYNdMo1Pifo9WKBKvo4vGm205LkLd_0l_3CuBbYkzIv6pZMiX8UG97jAJACDSyojiIKefBTSNXAnHj0a10YFp'
    deviceToken = device_token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }

    body = {
        'notification': {'title': 'Order completed successfully',
                         },
        'to': deviceToken,
        'priority': 'high'
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))


def kitchen_notification(device_token):
    serverToken = 'AAAAyu8f9nE:APA91bH29nKGba3NpRs05RflAX9Zz6SLkcZqRPF-Q2a30pMBZoFRPHS4lx-7DoNa90a-oCzJpW5bJs4Q67AATGJXrdjqTZT4m4ab_Rnb3kkFF-tjoUAYqsIeWEU60DXcLFXjhtOpaAio'
    deviceToken = device_token

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }

    body = {
        'notification': {'title': 'Order completed successfully',
                         },
        'to': deviceToken,
        'priority': 'high'
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))


def payment_handler(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE order_order
                SET payment_status = %s
                WHERE id = %s"""
    conn = None
    order_id = data['order_id']

    if order_id:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT customer_customer.notification_token, order_order.restaurant_id, order_order.coffee_house_id  from order_order INNER JOIN customer_customer ON order_order.customer_id = customer_customer.id where order_order.id = {}".format(
                order_id))
        device_token = cur.fetchall()

        for token in device_token:
            restaurant_id = token['restaurant_id']
            coffee_house_id = token['coffee_house_id']
            if restaurant_id:
                conn = get_db()
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, device_token from kitchen_kitchenstaff where restaurant_id = {} ".format(restaurant_id))
                kitchen_staff_token = cur.fetchall()


            elif coffee_house_id:
                cur.execute("SELECT id , device_token from kitchen_kitchenstaff where coffee_house_id = {} ".format(
                    coffee_house_id))
                kitchen_staff_token = cur.fetchall()

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
        if updated_rows:
            message = "Order placed successfully"
            if device_token:
                for user_token in device_token:
                    user_notification(user_token['notification_token'])

            if kitchen_staff_token:
                for staff_token in kitchen_staff_token:
                    kitchen_notification(staff_token['device_token'])

        else:
            message = "Order not completed"
        return message

    elif data['payment_status'] == 'PAID':
        mollie_client = Client()
        mollie_client.set_api_key('test_sWt48EAPad4duS8WFqSPFjvCVGfePR')

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

                # for token in device_token:
                #     notification(token['notification_token'])

                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

            if updated_rows:
                message = "Order placed successfully"
                if device_token:
                    for user_token in device_token:
                        user_notification(user_token['notification_token'])

                if kitchen_staff_token:
                    for staff_token in kitchen_staff_token:
                        kitchen_notification(staff_token['device_token'])

            else:
                message = "Order not completed"
            return message

        else:
            updated_rows = 0
            payment_status = 'PENDING'
            try:
                conn = get_db()
                cur = conn.cursor()
                cur.execute(sql,
                            (payment_status, data['order_id']))
                updated_rows = cur.rowcount

                # for token in device_token:
                #     notification(token['notification_token'])

                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            if updated_rows:
                message = "Order placed successfully"

                if device_token:
                    for user_token in device_token:
                        user_notification(user_token['notification_token'])

                if kitchen_staff_token:
                    for staff_token in kitchen_staff_token:
                        kitchen_notification(staff_token['device_token'])
            else:
                message = "Order not completed"
            return message


def order(event):
    data = json.loads(event['body']) if event.get('body', 0) else event

    mollie_client = Client()
    mollie_client.set_api_key('test_sWt48EAPad4duS8WFqSPFjvCVGfePR')

    price = "{:.2f}".format(data['order_amount'])
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
    customer_id = data['customer_id']

    conn = get_db()
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT id,order_id from order_order ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()

    if row:
        fake_order_id = int(row['order_id']) + 1
    else:
        fake_order_id = 1

    if data['order_type'] == "DeliveryStatus":
        order_type = "DELIVERY"
    elif data['order_type'] == "PickupStatus":
        order_type = "PICKUP"
    elif data['order_type'] == "Dining":
        order_type = "DINING"

    if data.get('order_amount'):

        payment_status = "PENDING"
        order_status = "PENDING"
        total_amount = data['order_amount']

        cur = conn.cursor()
        # conn.autocommit = True
        cur.execute(
            "insert into order_order(order_id, order_amount, order_status, payment_status, payment_id, delivery_address, postcode, city, waiter_tips, order_type, delivery_time, date_time, customer_id, coffee_house_id, restaurant_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
            (fake_order_id,
             data['order_amount'],
             order_status,
             payment_status,
             payment_id,
             data['delivery_address'],
             data['postcode'],
             data['city'],
             data['waiter_tips'],
             order_type,
             data['delivery_time'],
             data['date_time'],
             customer_id,
             data['coffee_house_id'],
             data['restaurant_id']))

        get_id = cur.fetchone()
        current_order_id = get_id['id']

        if data.get('food_list'):
            object_list = data.get('food_list')
            for food_items in object_list:
                cur.execute(
                    "insert into order_restaurantorder(food_quantity, food_note, food_id, order_id, item_total) values(%s,%s,%s,%s,%s) RETURNING id;",
                    (food_items['CountItem'],
                     # food_items['variant_quantity'],
                     food_items['food_note'],
                     food_items['id'],
                     # food_items['food_variant_id'],
                     current_order_id,
                     food_items['item_total'],
                     ))
                food_item_id = cur.fetchone()
                food_id = food_item_id['id']

                food_addons = food_items['food_addons']

                if food_addons:
                    for addon in food_addons:
                        cur.execute(
                            "insert into order_restaurantorderaddon(addon_quantity, item_total, food_addon_id, order_id) values(%s,%s,%s,%s)",
                            (addon['addon_quantity'],
                             addon['item_total'],
                             addon['id'],
                             current_order_id
                             ))

            conn.commit()
            conn.close()


        elif data.get('coffee_list'):
            object_list = data.get('coffee_list')
            for coffee_items in object_list:
                cur.execute(
                    "insert into order_coffeeorder(coffee_quantity, coffee_note, coffee_id, order_id,item_total) values(%s,%s,%s,%s,%s) RETURNING id;",
                    (coffee_items['CountItem'],
                     coffee_items['coffee_note'],
                     coffee_items['id'],
                     current_order_id,
                     coffee_items['item_total']
                     ))
                coffee_item_id = cur.fetchone()
                coffee_id = coffee_item_id['id']

                coffee_addons = coffee_items['coffee_addons']

                if coffee_addons:
                    for addon in coffee_addons:
                        cur.execute(
                            "insert into order_coffeeaddonorder(addon_quantity, item_total, coffee_addons_id, order_id) values(%s,%s,%s,%s)",
                            (addon['addon_quantity'],
                             addon['item_total'],
                             addon['id'],
                             current_order_id
                             ))
            conn.commit()
            conn.close()

    if data['restaurant_id']:
        property = data['restaurant_id']
        name_of_property = 'restaurants'

    elif data['coffee_house_id']:
        property = data['coffee_house_id']
        name_of_property = 'coffee_houses'

    return {
        'body': {
            "order_id": current_order_id,
            "checkout": payment['_links']['checkout']['href'],
            "{}".format(name_of_property): property
        }
    }


def address_update(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE order_order
                SET delivery_address = %s, postcode = %s, city = %s
                WHERE id = %s """
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

    if updated_rows:

        message = "Order placed successfully"
    else:
        message = "Order not completed"
    return message

    # return updated_rows


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

    if data.get('order_amount'):
        response = order(event)
        table_status(event)
        return response

    elif data.get('order_id'):
        payment_response = payment_handler(event)
        return {
            'body': payment_response
        }
    elif data.get('update_delivery_address'):
        delivery_address_update = address_update(event)
        return {
            'body': delivery_address_update
        }

    else:
        return {
            'statusCode': "error"
        }

