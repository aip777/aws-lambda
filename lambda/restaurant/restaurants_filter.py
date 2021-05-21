import json
from math import cos, asin, sqrt
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


def closest(data, v):
    return min(data, key=lambda p: distance(v['latitude'], v['longitude'], p['latitude'], p['longitude']))


def get_data():
    conn = get_db()
    curr = conn.cursor()
    curr.execute("SELECT latitude, longitude from restaurant_restaurants")

    # curr.execute("select * from (SELECT  *,( 3959 * acos( cos( radians(6.414478) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians(12.466646) ) + sin( radians(6.414478) ) * sin( radians( latitude ) ) ) ) AS distance FROM restaurant_restaurants) al where distance < 5 ORDER BY distance LIMIT 1100;")
    row = curr.fetchall()
    return row


def lambda_handler(event, context):
    tst = get_data()
    tempDataList = get_data()
    data = json.loads(event['body']) if event.get('body', 0) else event

    # v = {'lat': 39.76, 'lon': -86.0}
    results = closest(tempDataList, data)

    # TODO implement
    return {
        'statusCode': 200,
        'body': results
    }
