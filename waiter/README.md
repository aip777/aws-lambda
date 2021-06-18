### Waiter login API

* POST request 
    API endpoint: https://fdtwhav026.execute-api.eu-central-1.amazonaws.com/default/waiter_login
    API key: 
  
    POST request for login
          {
                "email":"sajib@gmail.com",
                "password":"123456",
                "device_token":""
            }
            
    Response:
    {
    "body": {
        "id": 2,
        "first_name": "sajib saha",
        "last_name": "Cse",
        "date_of_birth": "2021-03-01",
        "profile_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/image.jpg",
        "address_line_1": "45 Nobel Extension",
        "address_line_2": "Voluptatum",
        "mobile": "122222",
        "city": "Dhaka",
        "state": "Dhakayyyy",
        "country": "BD",
        "zip_code": "2522",
        "is_active": true,
        "email": "sajib@gmail.com",
        "restaurant_id": 3,
        "coffee_house_id": 4
    }
}

### Table QR API
    API endpoint: https://rw2b5hkmh8.execute-api.eu-central-1.amazonaws.com/default/DiningTableQr
    API key: 

    POST Request QR
      {
        "qr_code": "5000"
      }

    Response
        {
          "body": {
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
            "latitude": 23.869757394903456,
            "longitude": 90.4164896761367,
            "restaurant_old_new_status": "Old",
            "type_of_restaurant": "INDIAN",
            "food_prepare_avg_time": "",
            "special_foods": "burger",
            "food_price_icon": "1",
            "restaurants_rating": 3.25,
            "total_customer_review": 4,
            "pickup_delivery_status": "pickup_and_delivery",
            "free_delivery": false,
            "offer": "88%",
            "status": "Open",
            "restaurant_active": true,
            "restaurant_email": "1",
            "id": 28,
            "table_name": "1",
            "number_of_seat": 2,
            "about_table": "rt",
            "coffee_house_id": null,
            "qr_code": "5000",
            "table_icon": "https://mapplate-public.s3.eu-central-1.amazonaws.com/Table-Icon/table2.png",
            "table_status": true,
            "is_active": true,
            "restaurant_id": 3
          }
        }

### POST Requests for table
    API endpoint: https://rw2b5hkmh8.execute-api.eu-central-1.amazonaws.com/default/DiningTableQr
    API key: 

    POST Request
    {
      "restaurant_id": 3
    }

    Response
            {
              "body": [
                {
                  "restaurant_name": "sajib restaurant",
                  "restaurant_phone": "01773546755",
                  "restaurant_about": "this is sajib restaurant",
                  "restaurant_address_line_1": "test1 coffeehouse",
                  "restaurant_address_line_2": "dhaka,Bangladesh",
                  "restaurant_profile_picture": "rst-profile-pic/restaurant_ljk1X9v.jpeg",
                  "restaurant_thumbnail": "rst-thumbnail-pic/thumbnail_e3g6jOV.jpeg",
                  "country": "BD",
                  "zip_code": "6400",
                  "city": "Dhaka",
                  "state": "Dhaka",
                  "latitude": 23.869757394903456,
                  "longitude": 90.4164896761367,
                  "restaurant_old_new_status": "Old",
                  "type_of_restaurant": "INDIAN",
                  "food_prepare_avg_time": "",
                  "special_foods": "burger",
                  "food_price_icon": "1",
                  "restaurants_rating": 3.25,
                  "total_customer_review": 4,
                  "pickup_delivery_status": "pickup_and_delivery",
                  "free_delivery": false,
                  "offer": "88%",
                  "status": "Open",
                  "restaurant_active": true,
                  "restaurant_email": "1",
                  "id": 28,
                  "table_name": "1",
                  "number_of_seat": 2,
                  "about_table": "rt",
                  "qr_code": "5000",
                  "table_icon": "https://mapplate-public.s3.eu-central-1.amazonaws.com/Table-Icon/table2.png",
                  "table_status": true,
                  "is_active": true,
                  "restaurant_id": 3
                },
                {
                  "restaurant_name": "sajib restaurant",
                  "restaurant_phone": "01773546755",
                  "restaurant_about": "this is sajib restaurant",
                  "restaurant_address_line_1": "test1 coffeehouse",
                  "restaurant_address_line_2": "dhaka,Bangladesh",
                  "restaurant_profile_picture": "rst-profile-pic/restaurant_ljk1X9v.jpeg",
                  "restaurant_thumbnail": "rst-thumbnail-pic/thumbnail_e3g6jOV.jpeg",
                  "country": "BD",
                  "zip_code": "6400",
                  "city": "Dhaka",
                  "state": "Dhaka",
                  "latitude": 23.869757394903456,
                  "longitude": 90.4164896761367,
                  "restaurant_old_new_status": "Old",
                  "type_of_restaurant": "INDIAN",
                  "food_prepare_avg_time": "",
                  "special_foods": "burger",
                  "food_price_icon": "1",
                  "restaurants_rating": 3.25,
                  "total_customer_review": 4,
                  "pickup_delivery_status": "pickup_and_delivery",
                  "free_delivery": false,
                  "offer": "88%",
                  "status": "Open",
                  "restaurant_active": true,
                  "restaurant_email": "1",
                  "id": 37,
                  "table_name": "1",
                  "number_of_seat": 6,
                  "about_table": "gbfv",
                  "qr_code": "5410KN",
                  "table_icon": "https://mapplate-public.s3.eu-central-1.amazonaws.com/Table-Icon/table6.png",
                  "table_status": false,
                  "is_active": true,
                  "restaurant_id": 3
                },
                {
                  "restaurant_name": "sajib restaurant",
                  "restaurant_phone": "01773546755",
                  "restaurant_about": "this is sajib restaurant",
                  "restaurant_address_line_1": "test1 coffeehouse",
                  "restaurant_address_line_2": "dhaka,Bangladesh",
                  "restaurant_profile_picture": "rst-profile-pic/restaurant_ljk1X9v.jpeg",
                  "restaurant_thumbnail": "rst-thumbnail-pic/thumbnail_e3g6jOV.jpeg",
                  "country": "BD",
                  "zip_code": "6400",
                  "city": "Dhaka",
                  "state": "Dhaka",
                  "latitude": 23.869757394903456,
                  "longitude": 90.4164896761367,
                  "restaurant_old_new_status": "Old",
                  "type_of_restaurant": "INDIAN",
                  "food_prepare_avg_time": "",
                  "special_foods": "burger",
                  "food_price_icon": "1",
                  "restaurants_rating": 3.25,
                  "total_customer_review": 4,
                  "pickup_delivery_status": "pickup_and_delivery",
                  "free_delivery": false,
                  "offer": "88%",
                  "status": "Open",
                  "restaurant_active": true,
                  "restaurant_email": "1",
                  "id": 40,
                  "table_name": "BFV",
                  "number_of_seat": 6,
                  "about_table": "jh",
                  "qr_code": "541770KN",
                  "table_icon": "https://mapplate-public.s3.eu-central-1.amazonaws.com/Table-Icon/table6.png",
                  "table_status": false,
                  "is_active": true,
                  "restaurant_id": 3
                },
                {
                  "restaurant_name": "sajib restaurant",
                  "restaurant_phone": "01773546755",
                  "restaurant_about": "this is sajib restaurant",
                  "restaurant_address_line_1": "test1 coffeehouse",
                  "restaurant_address_line_2": "dhaka,Bangladesh",
                  "restaurant_profile_picture": "rst-profile-pic/restaurant_ljk1X9v.jpeg",
                  "restaurant_thumbnail": "rst-thumbnail-pic/thumbnail_e3g6jOV.jpeg",
                  "country": "BD",
                  "zip_code": "6400",
                  "city": "Dhaka",
                  "state": "Dhaka",
                  "latitude": 23.869757394903456,
                  "longitude": 90.4164896761367,
                  "restaurant_old_new_status": "Old",
                  "type_of_restaurant": "INDIAN",
                  "food_prepare_avg_time": "",
                  "special_foods": "burger",
                  "food_price_icon": "1",
                  "restaurants_rating": 3.25,
                  "total_customer_review": 4,
                  "pickup_delivery_status": "pickup_and_delivery",
                  "free_delivery": false,
                  "offer": "88%",
                  "status": "Open",
                  "restaurant_active": true,
                  "restaurant_email": "1",
                  "id": 41,
                  "table_name": "BFV",
                  "number_of_seat": 8,
                  "about_table": "BDS",
                  "qr_code": "54W10KN",
                  "table_icon": "https://mapplate-public.s3.eu-central-1.amazonaws.com/Table-Icon/table8.png",
                  "table_status": false,
                  "is_active": true,
                  "restaurant_id": 3
                },
                {
                  "restaurant_name": "sajib restaurant",
                  "restaurant_phone": "01773546755",
                  "restaurant_about": "this is sajib restaurant",
                  "restaurant_address_line_1": "test1 coffeehouse",
                  "restaurant_address_line_2": "dhaka,Bangladesh",
                  "restaurant_profile_picture": "rst-profile-pic/restaurant_ljk1X9v.jpeg",
                  "restaurant_thumbnail": "rst-thumbnail-pic/thumbnail_e3g6jOV.jpeg",
                  "country": "BD",
                  "zip_code": "6400",
                  "city": "Dhaka",
                  "state": "Dhaka",
                  "latitude": 23.869757394903456,
                  "longitude": 90.4164896761367,
                  "restaurant_old_new_status": "Old",
                  "type_of_restaurant": "INDIAN",
                  "food_prepare_avg_time": "",
                  "special_foods": "burger",
                  "food_price_icon": "1",
                  "restaurants_rating": 3.25,
                  "total_customer_review": 4,
                  "pickup_delivery_status": "pickup_and_delivery",
                  "free_delivery": false,
                  "offer": "88%",
                  "status": "Open",
                  "restaurant_active": true,
                  "restaurant_email": "1",
                  "id": 30,
                  "table_name": "1",
                  "number_of_seat": 4,
                  "about_table": "lopoop",
                  "qr_code": "RED333p",
                  "table_icon": "https://mapplate-public.s3.eu-central-1.amazonaws.com/Table-Icon/table4.png",
                  "table_status": true,
                  "is_active": true,
                  "restaurant_id": 3
                }
              ]
            }