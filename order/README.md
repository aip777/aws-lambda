#### Order API

      API endpoint: https://3ugwckbnrc.execute-api.eu-central-1.amazonaws.com/default/foodOrder
      API key: 

      POST request for restaurant order
          {
            "order_amount": 130,
            "delivery_address": "Mirpur",
            "postcode": "1212",
            "city": "Dhaka",
            "waiter_tips": 12,
            "order_type": "DELIVERY",
            "delivery_time": "2021-03-04 02:18:07",
            "date_time": "2020-12-02T08:20:00.162Z",
            "customer_id": 2,
            "coffee_house_id": null,
            "restaurant_id": 2,
            "table": {
              "table_id": 30,
              "table_status": true
            },
            "food_list": [
              {
                "id": 3,
                "food_note": "Food Note",
                "CountItem": 4,
                "food_variant_id": 3,
                "variant_quantity": 5,
                "item_total": 120,
                "food_addons": [
                  {
                    "id": 1,
                    "addon_quantity": 3,
                    "item_total": 10
                  }
                ]
              }
            ]
          }
 
      Response
              {
                  "body": {
                      "order_id": 78,
                      "checkout": "https://www.mollie.com/paymentscreen/testmode/?method=creditcard&token=2.lmym04"
                  }
              }

      POST request for coffee order
            {
              "order_amount": 140,
              "delivery_address": "Mirpur",
              "postcode": "1212",
              "city": "Dhaka",
              "waiter_tips": 12,
              "order_type": "DELIVERY",
              "delivery_time": "2020-12-02T08:20:00.162Z",
              "date_time": "2020-12-02T08:20:00.162Z",
              "customer_id": 2,
              "coffee_house_id": 5,
              "restaurant_id": null,
              "table": {
                "table_id": 2,
                "table_status": true
              },
              "coffee_list": [
                {
                  "id": 5,
                  "coffee_note": "Food Note",
                  "coffee_quantity": 4,
                  "item_total": 120,
            
                  "coffee_addons": [
                    {
                      "id": 8,
                      "addon_quantity": 3,
                      "item_total": 20
                    }
                  ]
                }
              ]
            }

     Response

              {
                  "body": {
                      "order_id": 78,
                      "checkout": "https://www.mollie.com/paymentscreen/testmode/?method=creditcard&token=2.lmym04"
                  }
              }


     POST request for delivery address update
            {
              "order_id_num": 78,
              "update_delivery_address": "House 34, Gulshan 1, Dhaka 1212",
              "postcode": "1214",
              "city": "Mirpur Dhaka"
            }

    POST request for payment status

            {
              "order_id": 58,
              "payment_status": "PAID"
            }


### Order status update API
      API Url : https://tv4apvxjki.execute-api.eu-central-1.amazonaws.com/default/orderStatusForKitchen
      API Key : 
    
      POST request
      
        {
            "restaurant_id": 3
        }
    
      Response
    
          {
            "body": [
                {
                    "id": 400,
                    "order_id": "1",
                    "order_amount": 283.00,
                    "order_status": "COMPLETED",
                    "payment_status": "PAID",
                    "delivery_address": "",
                    "postcode": "",
                    "city": "",
                    "waiter_tips": 13.0,
                    "table_id": null,
                    "order_type": "DINING",
                    "delivery_time": "APR-01-2021 07:38AM",
                    "date_time": "APR-01-2021 07:38AM",
                    "customer_id": 17,
                    "coffee_house_id": null,
                    "restaurant_id": 3,
                    "customer": {
                        "id": 17,
                        "first_name": "tomi",
                        "last_name": "saha",
                        "customer_profile_pic": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/customer_profile_pic/140650334167744_customer_id_17.png",
                        "email": "sajibsahabdtask@gmail.com",
                        "address_line_1": "vbbh",
                        "address_line_2": "tyt",
                        "mobile": "+88001785-566666"
                    },
                    "restaurant": {
                        "id": 3,
                        "restaurant_name": "sajib restaurant",
                        "restaurant_phone": "01773546755",
                        "restaurant_about": "this is sajib restaurant",
                        "restaurant_address_line_1": "test1 coffeehouse",
                        "restaurant_address_line_2": "dhaka,Bangladesh",
                        "restaurant_profile_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/rst-profile-pic/restaurant_ljk1X9v.jpeg",
                        "restaurant_thumbnail": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/rst-thumbnail-pic/thumbnail_e3g6jOV.jpeg",
                        "country": "BD",
                        "zip_code": "6400",
                        "city": "Dhaka",
                        "state": "Dhaka",
                        "restaurant_linkedin": "",
                        "restaurant_website": "",
                        "restaurant_facebook": "",
                        "restaurant_instagram": "",
                        "restaurant_twitter": "",
                        "latitude": 33.0,
                        "longitude": 45.0,
                        "restaurant_old_new_status": "Old",
                        "type_of_restaurant": "INDIAN",
                        "food_prepare_avg_time": "",
                        "special_foods": "burger",
                        "food_price_icon": "1",
                        "restaurants_rating": 3.3333333333333335,
                        "total_customer_review": 3,
                        "pickup_delivery_status": "pickup_and_delivery",
                        "free_delivery": false,
                        "offer": "88%",
                        "status": "Open",
                        "restaurant_active": true,
                        "restaurant_email": "1"
                    },
                    "food_items": [
                        {
                            "id": 239,
                            "food_quantity": 1,
                            "variant_quantity": null,
                            "food_note": "",
                            "food_id": 7,
                            "food_variant_id": null,
                            "order_id": 400,
                            "item_total": 270.00
                        }
                    ],
                    "food": [
                        {
                            "id": 7,
                            "food_name": "Barger sajiv",
                            "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/image.jpg",
                            "food_price": 300.00,
                            "discount_type": 2,
                            "discount_price": 10.00,
                            "after_discount_price": 270.00,
                            "food_stock": 65,
                            "food_availability": "1",
                            "food_active": true,
                            "type_of_food": "bangla",
                            "food_components": "Wel getoast, Niet getoast, Wit and more",
                            "food_review": null,
                            "food_offer": null,
                            "food_details": "green green",
                            "restaurant_id": 10
                        }
                    ],
                    "food_variant": [],
                    "addon": []
                }
            ]
        }     

    POST request for status update
    
            {
              "order_id": 388,
              "status": "IN_PROGRESS",
              "restaurant_id": 3
            }

    POST request for table update
            {
              "order_id": 496,
              "table_status": true,
              "table_id": 30
            }
    
 