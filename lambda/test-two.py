import requests
import json

serverToken = 'AAAAmrmFsT0:-OAO7'

deviceToken = 'fDKBb8JDQp6jlBiSQXOKJL:'

headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
      }

body = {
          'notification': {'title': 'Order in progress HHHH',
                            'body': 'Order completed'
                           },
          'to':deviceToken,
          'priority': 'high'
        }
response = requests.post("https://fcm.googleapis.com/fcm/send", headers = headers, data=json.dumps(body))
print(response.status_code)
print(response.json())
