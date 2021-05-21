### Restaurants API
    API endpoint: https://6g94vp2gd1.execute-api.eu-central-1.amazonaws.com/default/restaurantProfile
    API key: 
    
    POST Request
    {
      "latitude": 23.771684,
      "longitude": 90.419284
    }    

    Response
            {
              "body": [
                {
                  "id": 6,
                  "restaurant_name": "Aronnok Restaurant",
                  "restaurant_email": "",
                  "restaurant_phone": "0147258369",
                  "restaurant_about": "",
                  "restaurant_address_line_1": "Dhaka",
                  "restaurant_address_line_2": "Dhaka",
                  "restaurant_profile_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/rst-profile-pic/res3.jpeg",
                  "restaurant_thumbnail": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/rst-thumbnail-pic/res15_PIQiGLD.jpeg",
                  "country": "BD",
                  "zip_code": "1212",
                  "city": "Dhaka",
                  "state": "Dhaka",
                  "latitude": 23.79055505931975,
                  "longitude": 90.37553561139826,
                  "restaurant_old_new_status": "New",
                  "type_of_restaurant": "",
                  "food_prepare_avg_time": "",
                  "special_foods": "tt",
                  "food_price_icon": "1",
                  "status": "Open",
                  "restaurant_active": true,
                  "restaurants_rating": null,
                  "total_customer_review": null,
                  "pickup_delivery_status": "pickup_and_delivery",
                  "free_delivery": false,
                  "offer": ""
                },
                {
                  "id": 12,
                  "restaurant_name": "green restaurant",
                  "restaurant_email": "",
                  "restaurant_phone": "017334345435",
                  "restaurant_about": "this restaurant is good and very popular.",
                  "restaurant_address_line_1": "comilla",
                  "restaurant_address_line_2": "dhaka",
                  "restaurant_profile_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/rst-profile-pic/istockphoto-1137365972-612x612.jpg",
                  "restaurant_thumbnail": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/rst-thumbnail-pic/istockphoto-1137365972-612x612.jpg",
                  "country": "AF",
                  "zip_code": "34433",
                  "city": "dhaka",
                  "state": "sdfsdf",
                  "latitude": 23.790618028701655,
                  "longitude": 90.3755481810111,
                  "restaurant_old_new_status": "New",
                  "type_of_restaurant": "FAST FOOD",
                  "food_prepare_avg_time": "",
                  "special_foods": "barger",
                  "food_price_icon": "1",
                  "status": "Open",
                  "restaurant_active": true,
                  "restaurants_rating": null,
                  "total_customer_review": null,
                  "pickup_delivery_status": "pickup_and_delivery",
                  "free_delivery": true,
                  "offer": "20%"
                }
              ]
            }

### FOOD API 
    API endpoint: https://6e4fqjwvbj.execute-api.eu-central-1.amazonaws.com/default/foods
    API key: 

    POST Request
    {
      "restaurant_id": 3
    }

    Response
    {
      "body": [
        {
          "id": 92,
          "food_name": "Chines Chicken",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/coffee.jpeg",
          "food_price": 140.01,
          "discount_type": 1,
          "discount_price": 10.01,
          "after_discount_price": 130,
          "food_stock": 10,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "indian",
          "food_components": "sugar",
          "food_review": null,
          "food_offer": "SS",
          "food_details": "great",
          "category_id": 6,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [],
          "category": "cold",
          "food_addon": []
        },
        {
          "id": 7,
          "food_name": "Barger sajiv",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/image.jpg",
          "food_price": 300,
          "discount_type": 2,
          "discount_price": 10,
          "after_discount_price": 270,
          "food_stock": 65,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "bangla",
          "food_components": "Wel getoast, Niet getoast, Wit and more",
          "food_review": null,
          "food_offer": null,
          "food_details": "green green",
          "category_id": 10,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [],
          "category": "indian",
          "food_addon": [
            {
              "id": 3,
              "addon_name": "Tomato sauce",
              "price": 56
            },
            {
              "id": 4,
              "addon_name": "green",
              "price": 56
            },
            {
              "id": 7,
              "addon_name": "Tomato sauce",
              "price": 55
            }
          ]
        },
        {
          "id": 29,
          "food_name": "new cheewats",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/istockphoto-1137365972-612x612_gD2tMet.jpg",
          "food_price": 45,
          "discount_type": 2,
          "discount_price": 45,
          "after_discount_price": 24.75,
          "food_stock": 45,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "new item",
          "food_components": "free suger",
          "food_review": null,
          "food_offer": null,
          "food_details": "this good to see",
          "category_id": 5,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [],
          "category": "indian",
          "food_addon": []
        },
        {
          "id": 30,
          "food_name": "chingora",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/istockphoto-1137365972-612x612_ivciaNg.jpg",
          "food_price": 45,
          "discount_type": 1,
          "discount_price": 4,
          "after_discount_price": 41,
          "food_stock": 45,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "new item",
          "food_components": "free suger",
          "food_review": null,
          "food_offer": null,
          "food_details": "this is very good",
          "category_id": 7,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [],
          "category": "indian",
          "food_addon": []
        },
        {
          "id": 8,
          "food_name": "cheews",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/photo-1552566626-52f8b828add9.jpg",
          "food_price": 200,
          "discount_type": 2,
          "discount_price": 10,
          "after_discount_price": 180,
          "food_stock": 56,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "hot soos",
          "food_components": "Wel getoast, Niet getoast, Wit and more",
          "food_review": null,
          "food_offer": null,
          "food_details": "green",
          "category_id": 9,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [
            {
              "id": 3,
              "variant_title": "green",
              "variant_price": 67
            },
            {
              "id": 1,
              "variant_title": "chili",
              "variant_price": 77
            }
          ],
          "category": "Barger",
          "food_addon": [
            {
              "id": 5,
              "addon_name": "potato",
              "price": 6
            },
            {
              "id": 6,
              "addon_name": "potato alo",
              "price": 78
            }
          ]
        },
        {
          "id": 31,
          "food_name": "greems",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/istockphoto-1137365972-612x612_AelLlmo.jpg",
          "food_price": 67,
          "discount_type": 1,
          "discount_price": 55,
          "after_discount_price": 12,
          "food_stock": 66,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "new item",
          "food_components": "free food",
          "food_review": null,
          "food_offer": null,
          "food_details": "this great food",
          "category_id": 7,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [],
          "category": "indian",
          "food_addon": []
        },
        {
          "id": 51,
          "food_name": "chaumin De",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/chicken_oH1QwlE.jpeg",
          "food_price": 123,
          "discount_type": 1,
          "discount_price": 33,
          "after_discount_price": 90,
          "food_stock": 0,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "Indian",
          "food_components": "FES",
          "food_review": null,
          "food_offer": null,
          "food_details": "FD",
          "category_id": 5,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [],
          "category": "indian",
          "food_addon": []
        },
        {
          "id": 91,
          "food_name": "new cold item",
          "food_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/food-picture/heart.png",
          "food_price": 45,
          "discount_type": 2,
          "discount_price": 4,
          "after_discount_price": 43.2,
          "food_stock": 45,
          "food_availability": "1",
          "food_active": true,
          "type_of_food": "green cond",
          "food_components": "super cream,another cream",
          "food_review": null,
          "food_offer": null,
          "food_details": "werwerwer",
          "category_id": 6,
          "food_time_id": null,
          "restaurant_id": 3,
          "variant": [],
          "category": "cold",
          "food_addon": []
        }
      ]
    }

### Food Addons
    API endpoint: https://vxh6d9sqj9.execute-api.eu-central-1.amazonaws.com/default/foodAddons
    API key: 
    
    POST Request
    {
      "food_name_id": "6"
    }
    
    Response
    {
      "statusCode": "error",
      "body": []
    }

### Restaurants Rating API
    API endpoint: https://nwcb9zi0yj.execute-api.eu-central-1.amazonaws.com/default/restaurantsRating
    API key: 

    POST Request for rating reataurant
    {
      "customer_rating": 3,
      "customer_id": 2,
      "restaurant_id": 3,
      "customer_comment": "Great"
    }

    Response
            {
              "body": {
                "restaurants_rating": 3.25,
                "customer_rating": {
                  "customer_id": 2,
                  "restaurant_id": 3,
                  "customer_rating": 3,
                  "customer_comment": "Great"
                }
              }
            }

    POST request for rating coffee house.

        {
          "customer_rating": 5,
          "customer_id": 2,
          "coffee_house_id": 4,
          "customer_comment": "Great"
        }
    
    Response
        {
          "body": {
            "coffee_house_rating": 5,
            "customer_rating": {
              "customer_id": 2,
              "coffee_house_id": 4,
              "customer_rating": 5,
              "customer_comment": "Great"
            }
          }
        }

