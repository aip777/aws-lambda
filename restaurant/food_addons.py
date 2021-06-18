import json
from rds.postgresql_rds import get_db


def get_foodaddons(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    curr = conn.cursor()
    curr.execute(
        "SELECT id,food_name_id, addon_name, price from food_foodaddons where food_name_id= {} ORDER BY id ASC".format(
            data['food_name_id']))

    row = curr.fetchall()
    return row


def lambda_handler(event, context):
    foodaddons = get_foodaddons(event)
    statusCode = ''
    if len(foodaddons) == 0:
        statusCode = "error"
    else:
        statusCode = "success"
    return {
        'statusCode': statusCode,
        "body": foodaddons
    }