import json
body = {
    "order_id": 316,
    "checkout": "asdf",
    "coffee_house": 4
}

if body.get('coffee_house'):
    print("coffee_house")

elif body.get('restaurant'):
    print("restaurant")