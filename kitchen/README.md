### Kitchen staff login API
    API endpoint: https://9yjfq0kjw2.execute-api.eu-central-1.amazonaws.com/default/KitchenStaff?
    API key: 

    POST request for profile update
            {
              "id":1,
              "first_name": "ES Hossain",
              "last_name": "Khan",
              "to_char": "2024-01-15",
              "profile_picture": "",
              "address_line_1": "45 Nobel Extension",
              "address_line_2": "Voluptatum",
              "mobile": "122222",
              "city": "Dhaka",
              "state": "Dhaka",
              "country": "BD",
              "zip_code": "233",
              "password": "123456",
              "email": "sajib@gmail.com"
            }
      
    Response 
      {
            "body": {
                "id": 1,
                "first_name": "ES Hossain",
                "last_name": "Khan",
                "date_of_birth": "2024-01-15",
                "profile_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/kitchen_staff_profile_picture/fast-foods-candy-cookies-pastries-768.jpg",
                "address_line_1": "45 Nobel Extension",
                "address_line_2": "Voluptatum",
                "mobile": "122222",
                "city": "Dhaka",
                "state": "Dhaka",
                "country": "BD",
                "zip_code": "233",
                "is_active": true,
                "email": "sajib@gmail.com",
                "restaurant_id": 3,
                "coffee_house_id": 4
            }
        }
      
      POST request for login
            {
                "email":"sajib@gmail.com",
                "password":"123456",
                "device_token":""
            }
    
     Response
            {
                "body": {
                    "id": 1,
                    "first_name": "ES Hossain",
                    "last_name": "Khan",
                    "date_of_birth": "2024-01-15",
                    "profile_picture": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/kitchen_staff_profile_picture/fast-foods-candy-cookies-pastries-768.jpg",
                    "address_line_1": "45 Nobel Extension",
                    "address_line_2": "Voluptatum",
                    "mobile": "122222",
                    "city": "Dhaka",
                    "state": "Dhaka",
                    "country": "BD",
                    "zip_code": "233",
                    "is_active": true,
                    "email": "sajib@gmail.com",
                    "restaurant_id": 3,
                    "coffee_house_id": 4
                }
            }
            