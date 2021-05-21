import json
from rds.postgresql_rds import get_db
import psycopg2
from psycopg2.extras import RealDictConnection
import collections, functools, operator


def get_restaurants_rating(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    cur = conn.cursor()
    if data.get('restaurant_id') or data.get('restaurant_rating_id'):

        if data.get('restaurant_id'):
            restaurant_id = data.get('restaurant_id')
        elif data.get('restaurant_rating_id'):
            restaurant_id = data.get('restaurant_rating_id')

        cur.execute(
            "SELECT customer_rating from restaurant_restaurantratings where restaurant_id= {}".format(restaurant_id))
        row = cur.fetchall()
        items_len = len(row)
        result = dict(functools.reduce(operator.add, map(collections.Counter, row)))
        rating = result['customer_rating'] / items_len
        update_calculate_rating(event, rating, items_len)
        return rating

    elif data.get('coffee_house_id') or data.get('coffee_house_rating_id'):

        if data.get('coffee_house_id'):
            coffee_house_id = data.get('coffee_house_id')
        else:
            coffee_house_id = data.get('coffee_house_rating_id')

        cur.execute("SELECT customer_rating from coffeehouse_coffeehouseratings where coffee_house_id= {}".format(
            coffee_house_id))
        row = cur.fetchall()
        items_len = len(row)
        result = dict(functools.reduce(operator.add, map(collections.Counter, row)))
        rating = result['customer_rating'] / items_len
        update_calculate_rating(event, rating, items_len)
        return rating


def update_calculate_rating(event, rating, items_len):
    data = json.loads(event['body']) if event.get('body', 0) else event

    if data.get('restaurant_id'):
        sql = """ UPDATE restaurant_restaurants
                    SET restaurants_rating = %s, total_customer_review = %s
                    WHERE id = %s"""
        conn = None
        updated_rows = 0
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(sql,
                        (rating, items_len, data['restaurant_id']))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows

    elif data.get('coffee_house_id'):
        sql = """ UPDATE coffeehouse_coffeehouse
                    SET coffee_house_rating = %s, total_customer_review = %s
                    WHERE id = %s"""
        conn = None
        updated_rows = 0
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(sql,
                        (rating, items_len, data['coffee_house_id']))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows


def update_retaurant_review(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    if data.get('restaurant_id'):
        sql = """ UPDATE restaurant_restaurantratings
                    SET restaurant_id = %s, customer_rating = %s, customer_comment = %s
                    WHERE customer_id = %s"""
        conn = None
        updated_rows = 0
        try:
            conn = get_db()
            cur = conn.cursor()
            rep = '5'
            cur.execute(sql,
                        (data['restaurant_id'], data['customer_rating'], data['customer_comment'], data['customer_id']))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows

    elif data.get('coffee_house_id'):
        sql = """ UPDATE coffeehouse_coffeehouseratings
                    SET coffee_house_id = %s, customer_rating = %s, customer_comment = %s
                    WHERE customer_id = %s"""
        conn = None
        updated_rows = 0
        try:
            conn = get_db()
            cur = conn.cursor()
            rep = '5'
            cur.execute(sql,
                        (data['coffee_house_id'], data['customer_rating'], data['customer_comment'],
                         data['customer_id']))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return updated_rows


def insert_data(event):
    conn = get_db()
    data = json.loads(event['body']) if event.get('body', 0) else event

    if data.get('restaurant_id'):
        conn.autocommit = True
        curr = conn.cursor()
        curr.execute(
            "SELECT customer_id from restaurant_restaurantratings where customer_id= {}".format(data['customer_id']))
        row = curr.fetchone()
        if row == None:
            cur = conn.cursor()
            cur.execute(
                "insert into restaurant_restaurantratings(customer_rating, customer_id,customer_comment,restaurant_id ) values(%s,%s,%s,%s)",
                (data['customer_rating'],
                 data['customer_id'],
                 data['customer_comment'],
                 data['restaurant_id']
                 ))

        else:
            update_retaurant_review(event)

    elif data.get('coffee_house_id'):
        conn.autocommit = True
        curr = conn.cursor()
        curr.execute(
            "SELECT customer_id from coffeehouse_coffeehouseratings where customer_id= {}".format(data['customer_id']))
        row = curr.fetchone()
        if row == None:
            cur = conn.cursor()
            cur.execute(
                "insert into coffeehouse_coffeehouseratings(customer_rating, customer_id,customer_comment,coffee_house_id ) values(%s,%s,%s,%s)",
                (data['customer_rating'],
                 data['customer_id'],
                 data['customer_comment'],
                 data['coffee_house_id']
                 ))

        else:
            update_retaurant_review(event)


def get_rating(event):
    data = json.loads(event['body']) if event.get('body', 0) else event

    if data.get('restaurant_id'):
        conn = get_db()
        curr = conn.cursor()
        curr.execute(
            "SELECT customer_id, restaurant_id, customer_rating, customer_comment from restaurant_restaurantratings where customer_id={}".format(
                data['customer_id']))
        row = curr.fetchone()
        return row

    elif data.get('coffee_house_id'):
        conn = get_db()
        curr = conn.cursor()
        curr.execute(
            "SELECT customer_id, coffee_house_id, customer_rating, customer_comment from coffeehouse_coffeehouseratings where customer_id={}".format(
                data['customer_id']))
        row = curr.fetchone()
        return row


def get_all_customer_rating(event):
    data = json.loads(event['body']) if event.get('body', 0) else event

    if data.get('restaurant_rating_id'):
        conn = get_db()
        curr = conn.cursor()
        curr.execute(
            "SELECT customer_customer.first_name, customer_customer.last_name, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| customer_customer.customer_profile_pic AS customer_profile_pic, restaurant_restaurantratings.customer_id, restaurant_restaurantratings.restaurant_id, restaurant_restaurantratings.customer_rating, to_char(restaurant_restaurantratings.created_at, 'MON-DD-YYYY HH12:MIPM') AS created_at, restaurant_restaurantratings.customer_comment from restaurant_restaurantratings INNER JOIN customer_customer ON restaurant_restaurantratings.customer_id = customer_customer.id where restaurant_restaurantratings.restaurant_id={}".format(
                data['restaurant_rating_id']))

        row = curr.fetchall()
        if row:
            return row
        else:
            return []

    elif data.get('coffee_house_rating_id'):
        conn = get_db()
        curr = conn.cursor()
        curr.execute(
            "SELECT customer_customer.first_name, customer_customer.last_name, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| customer_customer.customer_profile_pic AS customer_profile_pic, coffeehouse_coffeehouseratings.customer_id, coffeehouse_coffeehouseratings.coffee_house_id, coffeehouse_coffeehouseratings.customer_rating, to_char(coffeehouse_coffeehouseratings.created_at, 'MON-DD-YYYY HH12:MIPM') AS created_at, coffeehouse_coffeehouseratings.customer_comment from coffeehouse_coffeehouseratings INNER JOIN customer_customer ON coffeehouse_coffeehouseratings.customer_id = customer_customer.id where coffeehouse_coffeehouseratings.coffee_house_id={}".format(
                data['coffee_house_rating_id']))
        row = curr.fetchall()
        if row:
            return row
        else:
            return []


def lambda_handler(event, context):
    data = json.loads(event['body']) if event.get('body', 0) else event
    # TODO implement
    insert_rating = insert_data(event)
    customer_rating = get_rating(event)

    if data.get('restaurant_id'):
        rating = 'restaurants_rating'
        restaurants_rating = get_restaurants_rating(event)
    elif data.get('coffee_house_id'):
        rating = 'coffee_house_rating'
        restaurants_rating = get_restaurants_rating(event)

    elif data.get('restaurant_rating_id') or data.get('coffee_house_rating_id'):
        all_customer_rating = get_all_customer_rating(event)
        total_rating = len(all_customer_rating)

        if all_customer_rating:
            if data.get('restaurant_rating_id'):
                rating = 'restaurants_rating'
                restaurants_rating = get_restaurants_rating(event)
            elif data.get('coffee_house_rating_id'):
                rating = 'coffee_house_rating'
                restaurants_rating = get_restaurants_rating(event)

            return {
                "body": {
                    "{}".format(rating): restaurants_rating,
                    "all_customer_rating": all_customer_rating,
                    "total_rating": total_rating
                }
            }
        else:
            return {
                "body": []
            }
    return {
        "body": {
            "{}".format(rating): restaurants_rating,
            "customer_rating": customer_rating
        }
    }
