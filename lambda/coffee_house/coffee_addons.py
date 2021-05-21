import json
from rds.postgresql_rds import get_db


def get_coffee_addons(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    try:
        curr = conn.cursor()
        curr.execute(
            "SELECT id, coffee_addon_name, coffee_addon_price, coffee_id from coffeehouse_coffeeaddons where coffee_id= {} ORDER BY id ASC".format(
                data['coffee_id']))
        coffee_addon_list = curr.fetchall()
        return coffee_addon_list
    except Exception as e:
        return e


def lambda_handler(event, context):
    coffee_addons = get_coffee_addons(event)
    statusCode = ''
    if len(coffee_addons) == 0:
        statusCode = "error"
    else:
        statusCode = "success"
    return {
        'statusCode': statusCode,
        "body": coffee_addons
    }
