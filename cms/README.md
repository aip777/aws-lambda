### Slider food offer API

    POST request
      API endpoint: https://f1u1nkh9a2.execute-api.eu-central-1.amazonaws.com/default/sliderFoodOffer
      API key:  
    
    Request 
        {
            "latitude": 23.869,
            "longitude": 90.416
        }
    Response
          {
              "body": {
                "food_offer_slider": [
                  {
                    "id": 9,
                    "food_name": "Barger sajiv",
                    "food_price": 300,
                    "discount_price": 7,
                    "after_discount_price": 279,
                    "slider_image": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/Slider_Images/fast-foods-candy-cookies-pastries-768_HUSbIzl.jpg",
                    "food_id": 7,
                    "restaurant_id": 3,
                    "slider_offer": 2
                  }
                ],
                "coffee_offer_slider": [
                  {
                    "id": 11,
                    "coffee_name": "nice hot Coffee",
                    "coffee_price": 500,
                    "discount_price": 7,
                    "coffee_offer": 2,
                    "slider_image": "https://mapplate-public.s3.eu-central-1.amazonaws.com/media/Slider_Images/istockphoto-1137365972-612x612.jpg",
                    "coffee_id": 5,
                    "coffee_house_id": 4,
                    "after_discount_price": 465
                  }
                ]
              } }
    